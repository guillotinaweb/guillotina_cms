


from guillotina import configure
from guillotina._settings import app_settings
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import ISchemaSerializeToJson
from guillotina.response import HTTPNotFound
from guillotina.utils import resolve_dotted_name
from os.path import join


@configure.service(
    context=IContainer, method='GET',
    permission='guillotina.ManageAddons', name='@tiles',
    summary='Install addon to container',
    parameters=[{
        "name": "body",
        "in": "body",
        "schema": {
            "$ref": "#/definitions/Addon"
        }
    }])
async def get_tiles(context, request):
    result = []
    for key, item in app_settings['available_tiles'].items():
        result.append({
            "@id": IAbsoluteURL(context) + join("@tiles" , item["name"]),
            "title": item['title'],
            "description": item['"description']
            })
    return result



@configure.service(
    context=IContainer, method='GET',
    permission='guillotina.ManageAddons', name='@tiles/{key}',
    summary='Install addon to container',
    parameters=[{
        "name": "body",
        "in": "body",
        "schema": {
            "$ref": "#/definitions/Schema"
        }
    }])
async def get_tile_schema(context, request):
    key = request.matchdict['key']
    if key not in app_settings['available_tiles'].keys():
        return HTTPNotFound()
    tile = app_settings['available_tiles'][key]
    schema = resolve_dotted_name(tile['schema'])
    return ISchemaSerializeToJson(shcema)
