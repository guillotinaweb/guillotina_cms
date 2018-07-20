
from guillotina.component import query_utility
from guillotina.interfaces import ICatalogUtility
from guillotina import testing
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager

import pytest
from pytest_docker_fixtures import images


ES_ENABLED = None

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

    if ES_ENABLED:
        if 'guillotina_elasticsearch' not in settings['applications']:
            settings['applications'].append('guillotina_elasticsearch')
    else:
        if 'guillotina_elasticsearch' in settings['applications']:
            settings['applications'].remove('guillotina_elasticsearch')


testing.configure_with(base_settings_configurator)


class CMSRequester(ContainerRequesterAsyncContextManager):
    def __init__(self, guillotina, loop):
        super().__init__(guillotina)

        # aioes caches loop, we need to continue to reset it
        search = query_utility(ICatalogUtility)
        if search:
            search.loop = loop
            if search._conn:
                search._conn.close()
            search._conn = None


@pytest.fixture(scope='function')
async def cms_requester(guillotina, loop):
    return CMSRequester(guillotina, loop)

@pytest.fixture(scope='function')
async def elasticsearch_enabled(elasticsearch):
    global ES_ENABLED
    ES_ENABLED = elasticsearch
    yield elasticsearch
    ES_ENABLED = False
