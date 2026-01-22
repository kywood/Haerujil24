from common_lib.Collections.ICollection import ICollection
from common_lib.Collections.cList import cList
from common_lib.MessageQueue.EventBus import IBus


class EventListenerContainer(ICollection):

    def __init__(self, event_bus: IBus):
        super().__init__()
        self._eventListenerContainer = cList()
        self._eventBus = event_bus
        pass

    # def Register(self, event_listener_name, event_listener):
    def AddListener(self, event_listener):
        # self._container.Put(event_listener_name, event_listener)
        self._eventListenerContainer.Put(event_listener)

    # def Register(self, event_listener_name, event_listener):
    #
    #     self._container.Put(event_listener_name, event_listener)

    def Start(self):

        for eventLister in self._eventListenerContainer:
            eventLister.Start()

    def Stop(self):

        for eventLister in self._eventListenerContainer:
            eventLister.Stop()

    def IsStoped(self):

        for eventLister in self._eventListenerContainer:
            if not eventLister.IsStoped():
                return False

        return True
