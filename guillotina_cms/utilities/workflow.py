import logging
from guillotina import app_settings
from guillotina_cms.interfaces import IWorkflowUtility
from guillotina import configure


logger = logging.getLogger('guillotina_cms')


@configure.utility(provides=IWorkflowUtility)
class WorkflowUtility:

    index_count = 0

    def __init__(self, settings={}, loop=None):
        self.loop = loop
        # self.workflows = app_settings['workflows']
        # self.workflows_content = app_settings['workflows_content']

    async def initialize(self, app):
        self.app = app

    async def finalize(self, app):
        pass
