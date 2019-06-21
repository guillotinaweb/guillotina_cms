import json

import pytest
from guillotina import testing
from guillotina.component import get_utility
from guillotina.interfaces import ICatalogUtility
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager
from pytest_docker_fixtures import images


images.configure(
    'elasticsearch',
    'docker.elastic.co/elasticsearch/elasticsearch', '6.8.0'
)


def base_settings_configurator(settings):
    if 'applications' in settings:
        settings['applications'].append('guillotina_cms')
    else:
        settings['applications'] = ['guillotina_cms']


testing.configure_with(base_settings_configurator)


class CMSRequester(ContainerRequesterAsyncContextManager):
    def __init__(self, guillotina, loop):
        super().__init__(guillotina)

        # aioes caches loop, we need to continue to reset it
        search = get_utility(ICatalogUtility)
        search.loop = loop
        if getattr(search, '_conn', None):
            search._conn.close()
        search._conn = None

    async def __aenter__(self):
        await super().__aenter__()
        await self.requester('POST', '/db/guillotina/@addons', data=json.dumps({
            'id': 'cms'
        }))
        return self.requester


@pytest.fixture(scope='function')
async def cms_requester(elasticsearch, guillotina, loop):
    from guillotina import app_settings
    yield CMSRequester(guillotina, loop)
