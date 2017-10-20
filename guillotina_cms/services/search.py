# -*- encoding: utf-8 -*-
from guillotina.api.service import Service
from guillotina import configure
from guillotina.interfaces import IContainer

SECRET = 'secret'


@configure.service(
    context=IContainer, method='GET',
    permission='guillotina.AccessContent', name='@search',
    summary='Search')
class Search(Service):

    __allow_access__ = True

    async def __call__(self):
    	return []