# -*- encoding: utf-8 -*-
from guillotina.api.service import Service
from datetime import datetime, timedelta
import jwt
from aiohttp.web import Response
from guillotina.interfaces import IDownloadView
from zope.interface import alsoProvides
from guillotina import configure
from guillotina.interfaces import IContainer

SECRET = 'secret'


@configure.service(
    context=IContainer, method='POST',
    permission='guillotina.AccessContent', name='@login',
    summary='Components for a resource')
class Login(Service):

    __allow_access__ = True

    async def __call__(self):
        ttl = 3660
        token = jwt.encode(
            {
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(seconds=ttl),
                'fullname': 'root',
                'sub': 'root'
            },
            SECRET,
            algorithm='HS256')
        return {
            'token': token.decode('utf-8')
        }


@configure.service(
    context=IContainer, method='POST',
    permission='guillotina.AccessContent', name='@refresh',
    summary='Components for a resource')
class Refresh(Service):

    def __init__(self, context, request):
        super(Refresh, self).__init__(context, request)
        alsoProvides(self, IDownloadView)

    async def __call__(self):
        ttl = 3660
        token = jwt.encode(
            {
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(seconds=ttl),
                'token': 'YWRtaW4='
            },
            SECRET,
            algorithm='HS256')
        return Response(body=token)
