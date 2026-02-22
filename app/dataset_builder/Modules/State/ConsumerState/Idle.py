# import time
from typing import Any

from Defines.StateDefine import StateDefine
from Modules.State.State import abState

class IdleState(abState):

    def __init__(self,stateController ):
        super().__init__(stateController , StateDefine.ConsumerState.E_STATE.Idle)

    def Enter(self, stateEnterData :Any = None):
        print("IdleState::Enter")
        pass


    def Leave(self):
        print("IdleState::Leave")
        pass

    def Proc(self):
        print(f"IdleState::Proc")

        # 잡이 있는지 확인을 하자....
        from Modules.Utils.S3Utils import S3Utils
        import time
        from Factory.MinioConnectionFactory import MinioConnectionFactory

        # while True:
        #     print("=====")
        #     time.sleep(2)
        #
        parentProcess = self.GetParentProcess()
        configLoader = parentProcess.GetConfigLoader()

        from Modules.Extrator.ExtractorUtils import ExtractorUtils
        s3UnnormalDir = ExtractorUtils.GetS3UnNormalDirName(configLoader)

        try:
            minioConnection = MinioConnectionFactory.GetConnection(
                configLoader
            )
        except Exception as e:
            import traceback
            print("MinIO connection failed:", e)
            traceback.print_exc()
            raise e

        while True:

            unNormalLists = S3Utils.GetUnNormalLists(minioConnection, s3UnnormalDir)

            unNormalListsLength =  len(unNormalLists)

            if unNormalListsLength <= 0 :
                print("Not Found Wait For UnNormal File")
                time.sleep(5)
                pass
            else:

                self.GetStateController().ChangeState(
                    state_id=StateDefine.ConsumerState.E_STATE.Dispatching ,
                    stateEnterData =unNormalLists
                )

                return

