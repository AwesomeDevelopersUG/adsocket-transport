import json
import redis

from . import BaseBroker


class Redis(BaseBroker):

    _r = None

    def __init__(self, channel='adsocket', host=None, port=None, max_connections=None, **kwargs):
        self._host = host or settings.REDIS_HOST
        self._port = port or settings.REDIS_PORT
        self._max_connections = max_connections or int(settings.REDIS_MAX_CONNECTIONS)
        self._channel = channel

    @property
    def _redis(self):
        if not self._r:
            self._r = redis.StrictRedis(
                host=self._host,
                port=self._port,
                max_connections=self._max_connections,
                decode_responses=True)
        return self._r

    def publish(self, message):
        self._redis.publish(self._channel, message.to_json())

    def store_credentials(self, key, data, ttl=None):
        """
        Store user authentication token to redis
        :param key:
        :param data:
        :param ttl:
        :return:
        """

        self._redis.set(key, json.dumps(data), ttl)


broker = Redis