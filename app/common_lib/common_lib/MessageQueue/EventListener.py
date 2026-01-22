from abc import abstractmethod

from common_lib.Thread.abThreading import abThreading


class ListenThread(abThreading):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def runAct(self):
        pass

    @abstractmethod
    def preProcessing(self):
        pass

    @abstractmethod
    def postProcessing(self):
        pass

class EventListener(ListenThread):

    def __init__(self):
        # IListrner.__init__(self)
        ListenThread.__init__(self)
        from common_lib.Collections.cDict import cDict
        self._channelContainer = cDict()
        self._messageHandler = None

        self._eventBus = None

        pass

    def SetEventBus(self, event_bus):
        self._eventBus = event_bus

    def SetMessageHandler(self, message_handler):
        self._messageHandler = message_handler
        return self

    def AppendChannels(self, message_channels: list):
        for message_channel in message_channels:
            self._channelContainer.Put(message_channel.GetChannelName(), message_channel)
        return self

    def AppendChannel(self, message_channel):
        # self._channelCounter,Put(message_channel)
        self._channelContainer.Put(message_channel.GetChannelName(), message_channel)
        return self

    def preProcessing(self):
        pass

    def postProcessing(self):
        pass

    def HandleThread(self):
        print("abThreading ")
        pass

    # @abstractmethod
    def run(self):

        try:

            self.preProcessing()

            # while not self.IsStopReq():
            while not self.IsStop():
                try:
                    print("-------------")

                    self.runAct()
                except Exception as e:
                    print(f" except Exception as e : {e}")
                    pass

            # from ody_lib.threads.abThread import abThread

            from common_lib.Thread.abThread import E_THREAD_STATUS
            self.setThreadStatus(E_THREAD_STATUS.STOPPED)
            self.postProcessing()
        except Exception as e:
            print(f"=================== parent process error Throw Begin ===================")
            self._eventBus.GetParentProcess().TryException(e)
            print(f"=================== parent process error Throw End ===================")
            self.Stop()
            # from ody_lib.threads.abThread import abThread
            from common_lib.Thread.abThread import abThread
            self.setThreadStatus(abThread.E_THREAD_STATUS.STOPPED)
            raise e

    # @abstractmethod
    def runAct(self):
        ## 이부분에선 queue 를 선회 하면서
        
        import time
        import json
        
        for channel_name in self._channelContainer:


            # print(f"runAct :: channel_name:{channel_name}")

            messageChannel = self._channelContainer.Get(channel_name)

            # print(f">>>>>>>>>>>>>>>>>>runAct :: channel_name:{channel_name}")

            # messageChannel = self._channelContainer[channel_name]
            protocol = messageChannel.Pop()

            # print(f">>>>>>>>>>>>>>>>>>runAct protocol :: channel_name:{channel_name} {protocol}")

            if protocol == None:
                time.sleep(2)
                continue

            # print(f" eventListener : runAct : chnm : {channel_name} P : {protocol}")

            print(f" [Recv] protocol : {protocol}")

            # jsons = json.loads(protocol)

            ## 해당 부분에서 protocolid 를 따기 위한드이나
            ## 이부분이 좀~~~ 문제있음 protocolId 직접쓰고 있음
            # pid = jsons['protocolId']
            # print(pid)
            #
            # handler = self._messageHandler.GetHandler(pid)
            # if handler == None:
            #     continue
            #
            # handler(protocol)
        
            time.sleep(0.1)

        pass
    pass