


from zope.interface import Interface
from guillotina import configure


@configure.tile(
  name="title",
  title="Title",

)
class ITitle(Interface):

