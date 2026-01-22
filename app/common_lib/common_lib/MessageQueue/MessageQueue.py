from abc import abstractmethod


class IMessageQueue:

    def __init__(self):
        pass

    @abstractmethod
    def Push(self, channel_name, protocol):
        pass

    @abstractmethod
    def Pop(self, channel_name):
        pass

    @abstractmethod
    def Peek(self, channel_name):
        pass

    @abstractmethod
    def Count(self, channel_name):
        pass

    @abstractmethod
    def InitLock(self, channel_name):
        pass

class abMessageQueue(IMessageQueue):
    def __init__(self,
                 message_queue_source
                 ):
        super().__init__()

        self._messageQueueSource = message_queue_source

        pass

    def _getSource(self):
        return self._messageQueueSource

    @abstractmethod
    def InitLock(self, channel_name):
        pass

    pass

## redis 를 주입 받자......

class RedisMessageQueue(abMessageQueue):

    def __init__(self,
                 message_queue_source):
        super().__init__(message_queue_source)

        pass

    def _getSource(self):
        return self._messageQueueSource.GetRedis()

    def InitLock(self, channel_name):

        redis = self._getSource()

        # pp = redis.Ping()

        locknm = f"lock:{channel_name}"

        if redis.exists(locknm):
            redis.delete(locknm)

        return redis.lock(locknm, blocking=True)

    def Push(self, channel_name, protocol):
        self._getSource().lpush(channel_name, protocol)
        pass

    def Pop(self, channel_name):
        return self._getSource().rpop(channel_name)

    def Peek(self, channel_name):
        return self._getSource().lindex(channel_name, -1)

    def Count(self, channel_name):
        return self._getSource().llen(channel_name)

    pass

class RedisSentinelMessageQueue(abMessageQueue):

    def __init__(self,
                 message_queue_source):
        super().__init__(message_queue_source)

    def InitLock(self, channel_name):

        redisSentinel = self._getSource()
        locknm = f"lock:{channel_name}"

        if redisSentinel.Invoke(lambda redis: redis.exists(locknm)):
            redisSentinel.Invoke(lambda redis: redis.delete(locknm))

        return redisSentinel.Invoke(lambda redis: redis.lock(locknm, blocking=True))

    def Push(self, channel_name, protocol):
        self._getSource().Invoke(lambda redis: redis.lpush(channel_name, protocol))

    def Pop(self, channel_name):
        return self._getSource().rpop(channel_name)
        # return self._getSource().lindex(channel_name, -1)

    def Peek(self, channel_name):
        return self._getSource().Invoke(lambda redis: redis.lindex(channel_name, -1))
        # return self._getSource().lindex(channel_name, -1)

    def Count(self, channel_name):
        return self._getSource().Invoke(lambda redis: redis.llen(channel_name))
        # return self._getSource().llen(channel_name)

    pass
