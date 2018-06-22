from guillotina import configure
from guillotina.interfaces import IResource
from guillotina.component import query_utility
from guillotina.interfaces import ICatalogUtility
from guillotina.utils import get_content_path


@configure.service(
    context=IResource, method='GET', permission='guillotina.AccessContent', name='@search',
    summary='Make search request',
    parameters=[{
        "name": "q",
        "in": "query",
        "required": True,
        "type": "string"
    }],
    responses={
        "200": {
            "description": "Search results",
            "type": "object",
            "schema": {
                "$ref": "#/definitions/SearchResults"
            }
        }
    })
async def search_get(context, request):
    depth = request.query.get('path.depth')
    sort_on = request.query.get('sort_on')
    metadata = request.query.get('metadata_fields')
    b_size = request.query.get('b_size')
    search = query_utility(ICatalogUtility)
    if search is None:
        return {
            '@id': request.url.human_repr(),
            'items': [],
            'items_total': 0
        }
    result = await search.get_by_path(
        container=request.container,
        path=get_content_path(context))
    real_result = {
        '@id': request.url.human_repr(),
        'items': [],
        'items_total': result['items_count']
    }
    for member in result['member']:
        member['@id'] = member['@absolute_url']
        del member['@absolute_url']
    real_result['items'] = result['member']
    return real_result