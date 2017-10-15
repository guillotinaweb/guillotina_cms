from guillotina_cms.interfaces import IObjectWorkflow
from guillotina import configure
from guillotina.interfaces import IRequest
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IResource
from guillotina.interfaces import IDatabase
from guillotina.component import queryMultiAdapter
from guillotina.api.service import TraversableService


class Workflow(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request


@configure.service(
    context=IResource, method='GET',
    permission='guillotina.AccessContent', name='@workflow',
    summary='Workflows for a resource')
class WorkflowGET(TraversableService):

    async def publish_traverse(self, traverse):
        if len(traverse) == 1:
            # we want have the key of the registry
            self.value = queryMultiAdapter(
                (self.context, self.request),
                IObjectWorkflow, name=traverse[0])
            self.workflow_id = traverse[0]
        else:
            self.value = None
            self.workflow_id = None
        return self

    async def __call__(self):
        if not hasattr(self, 'value'):
            workflow = {
                'history': [],
                'transitions': []
            }
        else:
            obj_url = IAbsoluteURL(self.context, self.request)()
            workflow = {
                '@id': obj_url + '/@workflow/' + self.workflow_id,
                'items': await self.value()
            }
        return workflow


@configure.adapter(
    for_=(IResource, IRequest),
    provides=IObjectWorkflow,
    name='publish')
class Publish(Workflow):

    async def __call__(self):
        return None


@configure.adapter(
    for_=(IResource, IRequest),
    provides=IObjectWorkflow,
    name='submit')
class Submit(Workflow):

    async def __call__(self):
        return None
