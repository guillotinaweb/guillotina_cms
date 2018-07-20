# -*- coding: utf-8 -*-
from guillotina.i18n import MessageFactory
from guillotina import configure
from os import getenv
import logging

_ = MessageFactory('guillotina_cms')


app_settings = {
    'pubsub_connector': 'guillotina_cms.pubsub.RedisPubSubConnector',
    'commands': {
        'upgrade': 'guillotina_cms.commands.upgrade.UpgradeCommand'
    },
    'workflow': {
        'basic': {

        }
    }
}


def includeme(root):
    configure.scan('guillotina_cms.interfaces')
    configure.scan('guillotina_cms.api')
    configure.scan('guillotina_cms.behaviors')
    configure.scan('guillotina_cms.content')
    configure.scan('guillotina_cms.fields')
    configure.scan('guillotina_cms.json')
    configure.scan('guillotina_cms.utilities')
    configure.scan('guillotina_cms.vocabularies')
    configure.scan('guillotina_cms.permissions')
    configure.scan('guillotina_cms.install')
    configure.scan('guillotina_cms.validator')


    
sentry_dsn = getenv('SENTRY_DSN')
sentry_handler = None
if sentry_dsn:
    loggers = ['guillotina', 'guillotina_cms']
    # conditional import for little startup speed boost...
    import raven
    from raven.handlers.logging import SentryHandler
    import raven_aiohttp
    client = raven.Client(
        transport=partial(raven_aiohttp.QueuedAioHttpTransport, workers=2, qsize=1000))
    sentry_handler = SentryHandler(client)
    handler_factory = lambda: sentry_handler

    logger = logging.getLogger(logger_name)
    handler = handler_factory()
    logger.setLevel(config['level'])
    logger.addHandler(handler)
