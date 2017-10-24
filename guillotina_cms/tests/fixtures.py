from guillotina import testing
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager

import pytest


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


@pytest.fixture(scope='function')
async def cms_requester(elasticsearch, guillotina, loop):
    return CMSRequester(guillotina, loop)