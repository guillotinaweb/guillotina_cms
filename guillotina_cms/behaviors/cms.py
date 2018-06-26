from guillotina import configure
from guillotina.behaviors.instance import AnnotationBehavior
from guillotina_cms.interfaces import ICMSBehavior


@configure.behavior(
    title="CMS data behavior",
    provides=ICMSBehavior,
    for_="guillotina.interfaces.IResource")
class CMS(AnnotationBehavior):

    title = ContextProperty('title', None)
    creators = ContextProperty('creators', ())
    contributors = ContextProperty('contributors', ())
    creation_date = ContextProperty('creation_date', None)
    modification_date = ContextProperty('modification_date', None)

    # all properties but these 4 are not annotated
    __local__properties__ = ('creation_date', 'modification_date',
                             'creators', 'contributors', 'title')