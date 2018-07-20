from guillotina import testing
from guillotina.component import get_utility
from guillotina.interfaces import ICatalogUtility
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager

import json
import pytest

from pytest_docker_fixtures import images


images.configure(
    'elasticsearch',
    'docker.elastic.co/elasticsearch/elasticsearch-oss', '6.2.4'
)


def base_settings_configurator(settings):
    if 'applications' in settings:
        settings['applications'].append('guillotina_cms')
    else:
        settings['applications'] = ['guillotina_cms']

    settings["utilities"] = []


testing.configure_with(base_settings_configurator)


class CMSRequester(ContainerRequesterAsyncContextManager):
    def __init__(self, guillotina, loop):
        super().__init__(guillotina)

        # aioes caches loop, we need to continue to reset it
        search = get_utility(ICatalogUtility)
        search.loop = loop
        if search._conn:
            search._conn.close()
        search._conn = None

    async def __aenter__(self):
        try:
            await super().__aenter__()
        except:
            pass
        resp = await self.requester('POST', '/db/guillotina/@addons', data=json.dumps({
            'id': 'cms'
        }))
        return self.requester

@pytest.fixture(scope='function')
async def cms_requester(elasticsearch, guillotina, loop):
    return CMSRequester(guillotina, loop)