
class ThreadController:
    def __init__(self):
        self._threadLists={}
        pass

    def append(self,abThreadingControlled):
        k =abThreadingControlled.getName()
        self._threadLists[k]=abThreadingControlled

    def Start(self):
        for th in self._threadLists.values():
            th.Start()
            pass
        pass

    def Stop(self):
        for th in self._threadLists.values():
            th.Stop()
        pass

    def StopByName(self,thread_name):

        v=self._threadLists.get(thread_name)
        v.Stop()

        # for th in self.lists.values():
        #     th.Stop()
        pass

    def setException(self ,e , abThreadingControlled ):
        e=e
        print(e)