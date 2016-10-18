# -*- encoding: utf-8 -*-
from plone.server.api.service import Service


class Login(Service):

    async def __call__(self):
        return {
            'token': 'YWRtaW4='
        }
