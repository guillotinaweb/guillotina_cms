import logging


logger = logging.getLogger('guillotina_cms')


class WorkflowUtility:

    index_count = 0

    def __init__(self, settings={}, loop=None):
        self.loop = loop
        self.workflows = settings['workflows']
        self.workflows_content = settings['workflows_content']

    async def initialize(self, app):
        self.app = app

    async def finalize(self, app):
        pass
