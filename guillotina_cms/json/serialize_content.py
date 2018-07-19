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
