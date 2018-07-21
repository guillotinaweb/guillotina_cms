from guillotina import configure
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IFolder
from guillotina.interfaces import Interface
from guillotina.interfaces import IResource
from guillotina.interfaces import IResourceSerializeToJson
from guillotina.interfaces import IResourceSerializeToJsonSummary
from guillotina.json.serialize_value import json_compatible
from guillotina.json.serialize_content import SerializeToJson
from guillotina.json.serialize_content import SerializeFolderToJson


_tiles_key = 'guillotina_cms.tiles.behaviors.ITiles'


@configure.adapter(
    for_=(IResource, Interface),
    provides=IResourceSerializeToJsonSummary)
class DefaultJSONSummarySerializer(object):
    """Default ISerializeToJsonSummary adapter.

    Requires context to be adaptable to IContentListingObject, which is
    the case for all content objects providing IResource.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    async def __call__(self):

        summary = json_compatible({
            '@id': IAbsoluteURL(self.context)(),
            '@type': self.context.type_name,
            'title': self.context.title
        })
        return summary


def flat_itiles_behaviour(resource):
    if _tiles_key in resource:
            resource['tiles_layout'] = resource[_tiles_key]['tiles_layout']
            resource['tiles'] = resource[_tiles_key]['tiles']
    return resource


@configure.adapter(
    for_=(IResource, Interface),
    provides=IResourceSerializeToJson,
)
class CMSTilesSerializer(SerializeToJson):
    async def __call__(self, include=[], omit=[]):
        result = await super().__call__(include=include, omit=omit)
        return flat_itiles_behaviour(result)


@configure.adapter(
    for_=(IFolder, Interface),
    provides=IResourceSerializeToJson
)
class CMSTilesFolderSerializer(SerializeFolderToJson):
    async def __call__(self, include=[], omit=[]):
        result = await super().__call__(include=include, omit=omit)
        return flat_itiles_behaviour(result)






