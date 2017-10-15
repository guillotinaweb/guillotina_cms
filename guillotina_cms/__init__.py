# -*- coding: utf-8 -*-
from guillotina.i18n import MessageFactory
from guillotina import configure

_ = MessageFactory('guillotina_cms')


def includeme(root):
    configure.scan('guillotina_cms.install')
    configure.scan('guillotina_cms.services')
    configure.scan('guillotina_cms.content')
    configure.scan('guillotina_cms.validator')
