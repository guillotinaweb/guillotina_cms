from guillotina import configure
from guillotina.interfaces import IResourceSerializeToJson, IFolder, IContainer
from zope.interface import Interface
from guillotina.json.serialize_content import SerializeToJson, MAX_ALLOWED
from guillotina.interfaces import IInteraction
from guillotina.profile import profilable
from guillotina.component import get_multi_adapter
from guillotina.interfaces import IResourceSerializeToJsonSummary
from guillotina.interfaces import IResource
from guillotina.interfaces import IAbsoluteURL
from guillotina.json.serialize_value import json_compatible
from guillotina.directives import merged_tagged_value_list
from guillotina.interfaces import ISchemaSerializeToJson
from guillotina.json.serialize_schema import DefaultSchemaSerializer
from guillotina_cms.interfaces import ICMSLayer


@configure.adapter(
    for_=(IResource, ICMSLayer),
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


@configure.adapter(
    for_=(IFolder, ICMSLayer),
    provides=IResourceSerializeToJson)
class SerializeFolderToJson(SerializeToJson):

    @profilable
    async def __call__(self, include=[], omit=[]):
        result = await super(SerializeFolderToJson, self).__call__(
            include=include, omit=omit)

        security = IInteraction(self.request)
        length = await self.context.async_len()

        if length > MAX_ALLOWED or length == 0:
            result['items'] = []
        else:
            result['items'] = []
            async for ident, member in self.context.async_items(suppress_events=True):
                if not ident.startswith('_') and bool(
                        security.check_permission(
                        'guillotina.AccessContent', member)):
                    result['items'].append(
                        await get_multi_adapter(
                            (member, self.request),
                            IResourceSerializeToJsonSummary)())
        result['length'] = length
        result['is_folderish'] = True
        return result



@configure.adapter(
    for_=(IContainer, ICMSLayer),
    provides=IResourceSerializeToJson)
class SerializeContainerToJson(SerializeToJson):

    @profilable
    async def __call__(self, include=[], omit=[]):
        result = await super(SerializeFolderToJson, self).__call__(
            include=include, omit=omit)

        security = IInteraction(self.request)
        length = await self.context.async_len()

        if length > MAX_ALLOWED or length == 0:
            result['items'] = []
        else:
            result['items'] = []
            async for ident, member in self.context.async_items(suppress_events=True):
                if not ident.startswith('_') and bool(
                        security.check_permission(
                        'guillotina.AccessContent', member)):
                    result['items'].append(
                        await get_multi_adapter(
                            (member, self.request),
                            IResourceSerializeToJsonSummary)())
        result['length'] = length
        result['is_folderish'] = True
        return result