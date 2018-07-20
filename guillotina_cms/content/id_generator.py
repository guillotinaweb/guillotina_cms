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
from guillotina.interfaces import IIDGenerator
from guillotina.json.serialize_schema import DefaultSchemaSerializer
from guillotina_cms.interfaces import ICMSLayer


@configure.adapter(
    for_=(ICMSLayer),
    provides=IIDGenerator)
class IDGenerator(object):
    """Default IDGenerator adapter.

    Requires request to adapt on different layers. Returns the urls path id.
    """

    def __init__(self, request):
        self.request = request

    def __call__(self, data):

    	if 'title' in data:
    		new_title = data['title'].lower()
    		new_title.replace(' ', '-')
    		return new_title
    	else:
    		return None
