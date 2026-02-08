from abc import abstractmethod

from common_lib.Dtos.IDto import IDTO
from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE
from common_lib.MessageQueue.QueueType import E_QUEUE_TYPE


class ChannelDTO(IDTO):

    def __init__(self,
                 channel_name: str,
                 channel_type: E_CHANNEL_TYPE = E_CHANNEL_TYPE.NONE):
        super().__init__()
        self.channel_name = channel_name
        self.channel_type = channel_type
        pass


class ChannelQueueDTO(ChannelDTO):

    def __init__(self ,
                 channel_name : str ,
                 queue_type :E_QUEUE_TYPE ):
        super().__init__( channel_name=channel_name ,
                          channel_type=E_CHANNEL_TYPE.NONE )
        self.queueType=queue_type

    @abstractmethod
    def AssignQueue(self, mpMessageQueue ):

        pass


class ChannelQueueQueueDTO(ChannelQueueDTO):

    def __init__(self ,
                 channel_name : str  ):
        super().__init__( channel_name=channel_name ,
                          queue_type=E_QUEUE_TYPE.QUEUE )


    def AssignQueue( self , mpMessageQueue ):
        from common_lib.MessageQueue.PipeType import E_PIPE_TYPE
        from multiprocessing import Queue
        from multiprocessing import Lock

        channelInName = E_PIPE_TYPE.GetChannelName(self.channel_name, E_PIPE_TYPE.IN)
        channelOutName = E_PIPE_TYPE.GetChannelName(self.channel_name, E_PIPE_TYPE.OUT)

        from common_lib.MessageQueue.MessageQueueWrapper import MessageQueueWrapperQueue
        mpMessageQueue.GetQS()[channelInName] = MessageQueueWrapperQueue(Queue())
        mpMessageQueue.GetQS()[channelOutName] = MessageQueueWrapperQueue(Queue())

        mpMessageQueue.GetLocks()[channelInName] = Lock()
        mpMessageQueue.GetLocks()[channelOutName] = Lock()

        pass

class ChannelQueueHSetDTO(ChannelQueueDTO):

    def __init__(self ,
                 channel_name : str ):
        super().__init__( channel_name=channel_name ,
                          queue_type=E_QUEUE_TYPE.HSET )

    def AssignQueue(self , mpMessageQueue ):
        from multiprocessing import Lock
        from multiprocessing import Manager
        from common_lib.MessageQueue.MessageQueueWrapper import MessageQueueWrapperHSet
        mpMessageQueue.GetQS()[self.channel_name] = MessageQueueWrapperHSet(Manager().dict())
        mpMessageQueue.GetLocks()[self.channel_name] = Lock()


    pass