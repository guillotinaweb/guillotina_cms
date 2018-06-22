# -*- coding: utf-8 -*-
from guillotina import configure
from guillotina.api.service import Service
from guillotina.component import getMultiAdapter
from guillotina.component import getUtilitiesFor
from guillotina.component import queryUtility
from guillotina.interfaces import IResource
from guillotina.interfaces import IFactorySerializeToJson
from guillotina.interfaces import IResourceFactory
from guillotina.interfaces import IAbsoluteURL
from guillotina.response import HTTPNotFound


@configure.service(
    context=IResource, method='GET',
    permission='guillotina.AccessContent', name='@types/{type_id}',
    summary='Components for a resource',
    responses={
        "200": {
            "description": "Result results on types",
            "schema": {
                "properties": {}
            }
        }
    })
class Read(Service):

    async def prepare(self):
        type_id = self.request.matchdict['type_id']
        self.value = queryUtility(IResourceFactory, name=type_id)
        if self.value is None:
            raise HTTPNotFound(content={
                'reason': f'Could not find type {type_id}',
                'type': type_id
            })

    async def __call__(self):
        if not hasattr(self, 'value'):
            self.value = [x[1] for x in getUtilitiesFor(IResourceFactory)]
        if isinstance(self.value, list):
            result = []
            base_url = IAbsoluteURL(self.context, self.request)()
            for x in self.value:
                result.append({
                    '@id': base_url + '/@types/' + x.type_name,
                    'title': x.type_name
                })
        else:
            serializer = getMultiAdapter(
                (self.value, self.request),
                IFactorySerializeToJson)

            result = await serializer()
        return result
