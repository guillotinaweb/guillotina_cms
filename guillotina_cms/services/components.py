from guillotina_cms.interfaces import IObjectComponent
from guillotina import configure
from guillotina.interfaces import IRequest
from guillotina.interfaces import IAbsoluteURL
from guillotina.interfaces import IResource
from guillotina.interfaces import IDatabase
from guillotina.component import queryMultiAdapter
from guillotina.api.service import TraversableService


class Component(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request


@configure.service(
    context=IResource, method='GET',
    permission='guillotina.AccessContent', name='@components',
    summary='Components for a resource')
class ComponentsGET(TraversableService):

    async def publish_traverse(self, traverse):
        if len(traverse) == 1:
            # we want have the key of the registry
            self.value = queryMultiAdapter(
                (self.context, self.request),
                IObjectComponent, name=traverse[0])
            self.component_id = traverse[0]
        else:
            self.value = None
            self.component_id = None
        return self

    async def __call__(self):
        obj_url = IAbsoluteURL(self.context, self.request)()
        component = {
            '@id': obj_url + '/@components/' + self.component_id,
            'items': await self.value()
        }
        return component


@configure.adapter(
    for_=(IResource, IRequest),
    provides=IObjectComponent,
    name='breadcrumbs')
class Breadcrumbs(Component):

    async def __call__(self):
        result = []
        context = self.context
        while context is not None and not IDatabase.providedBy(context):
            result.append({
                'title': context.title,
                'url': IAbsoluteURL(context, self.request)()
            })
            context = getattr(context, '__parent__', None)
        result.reverse()
        return result


@configure.adapter(
    for_=(IResource, IRequest),
    provides=IObjectComponent,
    name='navigation')
class Navigation(Component):

    async def __call__(self):
        result = []
        container = self.request.container
        async for content in container.async_values():
            if IResource.providedBy(content):
                result.append({
                    'title': content.title,
                    'url': IAbsoluteURL(content, self.request)()
                })
        return result
