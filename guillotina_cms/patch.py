from guillotina import configure
from guillotina.interfaces import IResourceSerializeToJson, IFolder
from zope.interface import Interface
from guillotina.json.serialize_content import SerializeToJson, MAX_ALLOWED
from guillotina.interfaces import IInteraction
from guillotina.profile import profilable
from guillotina.component import get_multi_adapter
from guillotina.interfaces import IResourceSerializeToJsonSummary


@configure.adapter(
    for_=(IFolder, Interface),
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
