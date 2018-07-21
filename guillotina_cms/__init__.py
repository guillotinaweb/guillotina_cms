# -*- coding: utf-8 -*-
from guillotina.i18n import MessageFactory
from guillotina import configure
from guillotina._settings import app_settings

_ = MessageFactory('guillotina_cms')


app_settings = {
	'available_tiles': {}
}


def includeme(root):
    configure.scan('guillotina_cms.permissions')
    configure.scan('guillotina_cms.api')
    configure.scan('guillotina_cms.install')
    configure.scan('guillotina_cms.json')
    configure.scan('guillotina_cms.fields')
    configure.scan('guillotina_cms.content')
    configure.scan('guillotina_cms.validator')
    configure.scan('guillotina_cms.tiles')