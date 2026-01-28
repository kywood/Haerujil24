from abc import ABC
from common_lib.MessageQueue.MessageQueue import IMessageQueue


class IMessageQueueWrapper:


    def __init__(self):
        pass


    pass

class abMessageQueueWrapper(IMessageQueueWrapper , ABC):


    def __init__(self , queue ):
        super().__init__()
        self._queue = queue
        pass
    pass

class MessageQueueWrapperQueue(abMessageQueueWrapper):

    def __init__(self, queue):
        super().__init__(queue)


    pass


class MessageQueueWrapperHSet(abMessageQueueWrapper):

    def __init__(self, queue):
        super().__init__(queue)

    pass
