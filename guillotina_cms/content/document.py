# -*- encoding: utf-8 -*-
from guillotina import configure
from guillotina.content import Folder
from guillotina.interfaces import IFolder
from guillotina import schema
from guillotina_cms import _
from guillotina.directives import index


class IDocument(IFolder):

    index('text', type='text')
    text = schema.Text(
        title=_('Text'),
        required=False)


@configure.contenttype(
    type_name='Document',
    schema=IDocument,
    behaviors=['guillotina.behaviors.dublincore.IDublinCore'],
    allowed_types=[]  # dynamically calculated
)
class Document(Folder):
    pass
