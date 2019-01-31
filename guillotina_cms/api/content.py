from guillotina import configure
from guillotina.api.content import resolve_uid
from guillotina.catalog import index
from guillotina.db.interfaces import ICockroachStorage
from guillotina.db.interfaces import IPostgresStorage
from guillotina.interfaces import IAsyncContainer
from guillotina.interfaces import IContainer
from guillotina.response import HTTPBadRequest
from guillotina.response import HTTPPreconditionFailed
from guillotina.transactions import get_transaction
from guillotina.utils import get_behavior

from guillotina_cms.interfaces import ICMSBehavior


@configure.service(
    method='GET', name="resolveuid/{uid}", context=IContainer,
    permission='guillotina.AccessContent',
    summary='Get content by UID',
    responses={
        "200": {
            "description": "Successful"
        }
    })
async def plone_resolve_uid(context, request):
    '''
    b/w compatible plone endpoint name
    '''
    return await resolve_uid(context, request)


async def _move(parent, child_id, delta):
    ob = await parent.async_get(child_id)
    beh = await get_behavior(ob, ICMSBehavior)
    if beh.position_in_parent in (None, -1):
        raise HTTPPreconditionFailed(content={
            'message': f'Can not move `{child_id}`. No existing position found.'
        })
    beh.position_in_parent += delta
    await index.index_object(ob, indexes=['position_in_parent'], modified=True)
    return beh.position_in_parent


async def _swap(parent, one, two, order, mapped):
    one_pos = mapped[one]
    two_pos = mapped[two]

    ob_one = await parent.async_get(one)
    ob_two = await parent.async_get(two)

    beh_one = await get_behavior(ob_one, ICMSBehavior)
    beh_two = await get_behavior(ob_two, ICMSBehavior)

    beh_one.position_in_parent = two_pos
    beh_two.position_in_parent = one_pos

    one_idx = order.index(one)
    two_idx = order.index(two)
    order[two_idx], order[one_idx] = order[one_idx], order[two_idx]

    await index.index_object(ob_one, indexes=['position_in_parent'], modified=True)
    await index.index_object(ob_two, indexes=['position_in_parent'], modified=True)
    return {
        one: {
            'idx': two_idx,
            'pos': two_pos
        },
        two: {
            'idx': one_idx,
            'pos': one_pos
        }
    }


MAX_FOLDER_SORT_SIZE = 5000


@configure.service(
    context=IAsyncContainer, method='PATCH',
    permission='guillotina.ModifyContent', name='@order')
async def order_content(context, request):
    data = await request.json()
    subset_ids = data['subset_ids']
    delta = data['delta']

    # verify current order matches
    txn = get_transaction()
    if not IPostgresStorage.providedBy(txn.storage) or ICockroachStorage.providedBy(txn.storage):
        raise HTTPBadRequest(content={
            'message': 'Content ordering not supported'
        })

    conn = await txn.get_connection()
    results = await conn.fetch('''
select id, (json->>'position_in_parent')::int as pos from {}
WHERE parent_id = $1 AND of IS NULL
ORDER BY (json->>'position_in_parent')::int ASC
limit {}'''.format(
        txn.storage._objects_table_name, MAX_FOLDER_SORT_SIZE), context._p_oid)
    if len(results) >= MAX_FOLDER_SORT_SIZE:
        raise HTTPPreconditionFailed(content={
            'message': 'Content ordering not supported on folders larger than {}'.format(
                MAX_FOLDER_SORT_SIZE
            )
        })

    results.sort(key=lambda item: item['pos'] or 0)
    order = []
    mapped = {}
    for item in results:
        order.append(item['id'])
        mapped[item['id']] = item['pos']

    if len(subset_ids) > len(order):
        raise HTTPPreconditionFailed(content={
            'message': 'Invalid subset. More values than current ordering'
        })
    if len(subset_ids) == len(order):
        if subset_ids != order:
            raise HTTPPreconditionFailed(content={
                'message': 'Invalid subset',
                'current': order
            })
    else:
        # verify subset
        # find current ordered subset
        try:
            start = order.index(subset_ids[0])
            end = order.index(subset_ids[-1]) + 1
        except ValueError:
            raise HTTPPreconditionFailed(content={
                'message': 'Invalid subset. Could not calculate subset match',

            })
        order_subset = order[start:end]
        if subset_ids != order_subset:
            raise HTTPPreconditionFailed(content={
                'message': 'Invalid subset',
                'current': order_subset
            })

    if ((order.index(data['obj_id']) + delta + 1) > len(order) or (
            order.index(data['obj_id']) + delta) < 0):
        raise HTTPPreconditionFailed(content={
            'message': 'Can not move. Invalid move target.'
        })
    # now swap position for item
    moved_item_index = order.index(data['obj_id'])
    moved = {}
    # over range of delta and shift position of the rest the opposite direction
    # for example:
    #  - move idx 0, delta 3
    #    - idx 1, 2, 3 are moved to 0, 1, 2
    #  - move idx 4, delta -2
    #    - idx 2, 3 are moved to 3, 4
    if delta < 0:
        group = [i for i in reversed(
            order[moved_item_index + delta:moved_item_index + 1])]
    else:
        group = order[moved_item_index:moved_item_index + delta + 1]

    for item_id in group[1:]:
        moved.update(
            await _swap(context, data['obj_id'], item_id, order, mapped))

    return moved
