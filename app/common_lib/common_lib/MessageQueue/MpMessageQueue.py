from queue import Empty
from typing import List

from common_lib.MessageQueue.ChannelDTO import ChannelQueueDTO
from common_lib.MessageQueue.MessageQueue import abMessageQueue
from multiprocessing import Queue, Lock


class MpMessageQueue(abMessageQueue):
    def __init__(self, channel_queue_dtos : List[ChannelQueueDTO]):
        super().__init__(None)
        self._qs = {}     # channel_name -> Queue
        self._locks = {}  # channel_name -> Lock

        self._channelQueueDtos=channel_queue_dtos

        self._init()

    def _init(self):

        # qs = {"COMQ": Queue(),
        #       "COMQ_IN": Queue(),
        #       "COMQ_OUT": Queue(),
        #       }
        # locks = {"COMQ": Lock(),
        #          "COMQ_IN": Lock(),
        #          "COMQ_OUT": Lock(),
        #          }

        from common_lib.MessageQueue.PipeType import E_PIPE_TYPE

        for channelQueueDto in self._channelQueueDtos:

            ## TODO 1
            ## 이부분에서 반드시 해결해야 함....
            ## 음 queue_type 에 따라 생성되는 큐가 달라하함 펙토리에 이부분을 입력할것.....
            channelInName = E_PIPE_TYPE.GetChannelName(channelQueueDto.channel_name , E_PIPE_TYPE.IN)
            channelOutName = E_PIPE_TYPE.GetChannelName(channelQueueDto.channel_name , E_PIPE_TYPE.OUT)
            self._qs[ channelInName ] = Queue()
            self._qs[ channelOutName ] = Queue()

            self._locks[channelInName ] = Lock()
            self._locks[channelOutName ] = Lock()
            pass


        #
        # from common_lib.MessageQueue.PipeType import E_PIPE_TYPE
        # E_PIPE_TYPE.GetName(E_PIPE_TYPE.IN)
        #
        # from common_lib.MessageQueue.PipeType import E_PIPE_TYPE
        # E_PIPE_TYPE.GetName(E_PIPE_TYPE.IN)


        pass

    def _ensure(self, channel_name):

        pass

    # def _ensure(self, channel_name):
    #     if channel_name not in self._qs:
    #         self._qs[channel_name] = Queue()
    #         self._locks[channel_name] = Lock()

    def InitLock(self, channel_name):
        self._ensure(channel_name)
        return self._locks[channel_name]

    def Push(self, channel_name, protocol):
        self._ensure(channel_name)
        self._qs[channel_name].put(protocol)

    def Pop(self, channel_name):
        self._ensure(channel_name)
        try:
            # self.println()
            return self._qs[channel_name].get_nowait()
        except Empty:
            return None


    def Peek(self, channel_name):
        raise NotImplementedError("multiprocessing.Queue는 안전한 peek가 기본 제공 안됨")

    def Count(self, channel_name):
        # self._ensure(channel_name)
        # return len(self._qs[channel_name])
        raise NotImplementedError("qsize는 OS마다 부정확할 수 있음 (별도 카운터 권장)")


    def println(self):

        for key in self._qs.keys():
            v= self._qs.get(key)
            print(f" queue nm=:{key} ")
            # for el in v:


        pass