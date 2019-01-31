import datetime
from guillotina_cms.utils import get_last_child_position

from guillotina import configure
from guillotina.component import query_adapter
from guillotina.interfaces import IObjectAddedEvent
from guillotina.interfaces import IResource
from guillotina.security.utils import apply_sharing
from guillotina.utils import get_authenticated_user_id
from guillotina.utils import get_current_request
from guillotina_cms.interfaces import ICMSBehavior
from guillotina_cms.interfaces import IWorkflow
from guillotina.catalog import index


@configure.subscriber(
    for_=(IResource, IObjectAddedEvent),
    priority=1001)  # after indexing
async def cms_object_added(obj, event):
    cms = query_adapter(obj, ICMSBehavior)
    if cms is not None:
        request = get_current_request()
        user_id = get_authenticated_user_id(request)

        workflow = IWorkflow(obj)
        await cms.load(create=True)
        state = cms.review_state

        if 'set_permission' in workflow.states[state]:
            await apply_sharing(obj, workflow.states[state]['set_permission'])

        setattr(cms, 'history', [])
        cms.history.append(
            {
                'actor': user_id,
                'comments': '',
                'time': datetime.datetime.now(),
                'title': 'Created',
                'type': 'workflow',
                'data': {
                    'action': None,
                    'review_state': state,
                }
            }
        )
        cms._p_register()
        pos = await get_last_child_position(obj.__parent__) + 1
        cms.position_in_parent = pos
        fut = index.get_future()
        if obj.uuid not in fut.index:
            fut.index[obj.uuid] = {}
        fut.index[obj.uuid]['position_in_parent'] = cms.position_in_parent

    if hasattr(obj, 'title') and obj.title is None:
        obj.title = obj.id
