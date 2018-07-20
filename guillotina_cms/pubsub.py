from guillotina_rediscache import cache

import aioredis
import asyncio
import json
import logging


class RedisPubSubConnector:

    def __init__(self, channel_name):
        self.channel_name = channel_name

    async def initialize(self):
        pool = await cache.get_redis_pool()
        self.redis = aioredis.Redis(pool)
        channel, = await self.redis.subscribe(self.channel_name)
        self.channel = channel

    async def subscribe(self, callback):
        try:
            while (await self.channel.wait_message()):
                msg = await self.channel.get(encoding='utf-8')
                data = json.loads(msg)
                if data.get('ruid') != self.request.uid:
                    await callback(data)
        except asyncio.CancelledError as ex:
            await self.redis.unsubscribe(self.channel_name)
        except Exception as ex:
            logger.error(f'Problem with redis pubsub', exc_info=True)
        finally:
            try:
                await self.redis.unsubscribe(self.channel_name)
            except:
                pass

    async def publish(self, data):
        await self.redis.publish(self.channel, json.dumps(data))


class MockPubSubConnector:
    # global so we can mess with in tests...
    subscriptions = []
    published = []

    def __init__(self, channel_name):
        self.channel_name = channel_name

    async def initialize(self):
        pass

    async def subscribe(self, callback):
        self.subscriptions.append(callback)

    async def publish(self, data):
        self.published.append(data)
