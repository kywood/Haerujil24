import time
from typing import Any

from Defines.StateDefine import StateDefine
from Modules.State.State import abState


class AwaitingCompletionState(abState):


    def __init__(self,stateController):
        super().__init__(stateController,StateDefine.ConsumerState.E_STATE.AwaitingCompletion)

        self._messageChannelSet = None


    def Enter(self, stateEnterData :Any = None):
        print("AwaitingCompletionState::Enter")

        from Defines.Defines import Defines
        self._messageChannelSet = self.GetParentProcess().GetEventBus().GetMessageChannel(Defines.E_IPC.MAKE_SET)
        # vv= self._messageChannelSet.Get("unnormal/2026010901/movie_2.mp4")
        pass


    def Leave(self):
        print("AwaitingCompletionState::Leave")


    def IsComplete(self):
        hsetSocket = self._messageChannelSet.GetIPC().GetHSetSocket()
        for k in hsetSocket.keys():
            jobMarkProtocol = hsetSocket[k]

            # print(jobMarkProtocol.job_state ,jobMarkProtocol.file_path )
            if jobMarkProtocol.IsComplete() == False:
                return False

        return True


    def Proc(self):

        if self.IsComplete():
            ## 전부 완료 됐으니 이제 다시 아이들로 감..
            print(f"====================================  complete  wat 60 sec ====================================")
            time.sleep(180)

            self.GetStateController().ChangeState(
                state_id=StateDefine.ConsumerState.E_STATE.Idle
            )
        else:
            time.sleep(2)

    pass
