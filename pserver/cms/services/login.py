# -*- encoding: utf-8 -*-
from plone.server.api.service import Service
from datetime import datetime, timedelta
import jwt
from aiohttp.web import Response
from plone.server.interfaces import IDownloadView
from zope.interface import alsoProvides

SECRET = 'secret'


class Login(Service):

    def __init__(self, context, request):
        super(Login, self).__init__(context, request)
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
