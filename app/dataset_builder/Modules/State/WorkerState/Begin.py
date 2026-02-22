from Modules.State.State import abState
from Defines.StateDefine import StateDefine
from typing import Any


class BeginState(abState):

    def __init__(self,stateController ):

        super().__init__(stateController , StateDefine.WorkerState.E_STATE.Begin)

    def Enter(self, stateEnterData :Any = None):
        print("BeginState::Enter")
        pass


    def Leave(self):
        print("BeginState::Leave")
        pass

    def Proc(self):
        print(f"BeginState::Proc")

        ## 여기서 tmp 아래 만들자....
        from Modules.Extrator.ExtractorUtils import ExtractorUtils

        parentProces = self.GetParentProcess()
        configLoader = parentProces.GetConfigLoader()
        tmpDir = ExtractorUtils.GetTmpDirName(configLoader, parentProces.GetName())

        parentProces.SetTmpDir(tmpDir)

        # print(f"=========== :: BeginState :: dirnm :: {dirnm} " )
        #
        from pathlib import Path
        path = Path(tmpDir)
        path.mkdir(parents=True, exist_ok=True)

        self.GetStateController().ChangeState(
            state_id=StateDefine.WorkerState.E_STATE.Running
        )




