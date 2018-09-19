from guillotina import configure
from guillotina_cms.behaviors.syndication import ISyndicationSettings


@configure.service(
    context=ISyndicationSettings, method='GET',
    permission='guillotina.ViewContent', name='@feed',
    summary='RSS Feed')
async def feed(context, request):
    pass


@configure.service(
    context=ISyndicationSettings, method='GET',
    permission='guillotina.ViewContent', name='@rss',
    summary='RSS Feed')
async def rss(context, request):
    pass


@configure.service(
    context=ISyndicationSettings, method='GET',
    permission='guillotina.ViewContent', name='@atom',
    summary='Atom Feed')
async def atom(context, request):
    pass


@configure.service(
    context=ISyndicationSettings, method='GET',
    permission='guillotina.ViewContent', name='@itunes',
    summary='iTunes Feed')
async def itunes(context, request):
    pass
