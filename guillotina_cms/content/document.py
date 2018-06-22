# -*- encoding: utf-8 -*-
from guillotina import configure
from guillotina.content import Folder
from guillotina.interfaces import IFolder
from guillotina_cms.fields.richtext import RichTextField
from guillotina_cms import _
from guillotina.directives import index


class IDocument(IFolder):

    index('text', type='text')
    text = RichTextField(
        title=_('Text'),
        required=False,
        widget='richtext')


@configure.contenttype(
    type_name='Document',
    schema=IDocument,
    behaviors=['guillotina.behaviors.dublincore.IDublinCore'],
    allowed_types=[]  # dynamically calculated
)
class Document(Folder):
    pass
