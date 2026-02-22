import time
from typing import Any

from Defines.StateDefine import StateDefine
from Modules.Utils.S3Utils import S3Utils
from Modules.State.State import abState


class RunningState(abState):


    def __init__(self,stateController):
        super().__init__(stateController , StateDefine.WorkerState.E_STATE.Running)

        self._parentProcess = None
        self._jobQueue = None

    def Enter(self, stateEnterData :Any = None):
        print("RunningState::Enter")
        self._parentProcess = self.GetParentProcess()

        self._jobQueue = self._parentProcess.GetJobQueue()


        pass


    def Leave(self):
        print("RunningState::Leave")
        pass

    def ExtractProc(self , jobProtocol ):

        ## 이미지 추출하고

        ## TODO
        ## Down , .... 각각을 함수로 뽑자....


        processName = self._parentProcess.GetName()
        configLoader = self._parentProcess.GetConfigLoader()

        print(f"WorkerMessageHandler :: RunningState :: ExtractProc :: {processName} :: image down t u {jobProtocol.file_path} ")

        from Factory.MinioConnectionFactory import MinioConnectionFactory

        tmpDirName = self._parentProcess.GetTmpDir()

        s3Connection = MinioConnectionFactory.GetConnection(
            configLoader
        )

        from pathlib import Path
        tmpFileName = Path( tmpDirName ) /  jobProtocol.file_path

        S3Utils.DownloadFile(s3Connection ,jobProtocol.file_path , tmpFileName )

        from Modules.Extrator.ExtractorUtils import ExtractorUtils
        extractorPrefix = ExtractorUtils.GetExtractorPrefix(
            configLoader
        )


        from Modules.Extrator.ExtractorUtils import ExtractorUtils
        s3NormalDir = ExtractorUtils.GetS3NormalDirName(configLoader)


        src = Path(jobProtocol.file_path)
        # 첫 폴더 제거 후 새 루트로 붙이기
        sub_path = Path(*src.parts[1:-1])  # ('2026010900')
        out_path = Path(tmpDirName) / extractorPrefix / sub_path

        from Modules.Utils.FIleUtils import FileUtils
        FileUtils.MkDir( out_path )



        ## 이미지 변환
        # print(f"WorkerMessageHandler :: RunningState :: ExtractProc :: {processName} :: image transform {jobProtocol.file_path} ")
        #

        ## win 32 에서 더미 이미지를 만들어줌
        ## 000002.jpg
        import sys
        if sys.platform == "win32":
            from PIL import Image
            img = Image.new("RGB", (1, 1), color="black")

            # Path(out_path) / "000001.jpg"

            img.save(Path(out_path) / "000001.jpg")
            img.save(Path(out_path) / "000002.jpg")
            img.save(Path(out_path) / "000003.jpg")
            pass
        else:
            from Modules.Extrator.ImageExtractorStatic import ImageExtractorStatic
            extractorResults = ImageExtractorStatic.extract_fps(
                input_mp4=tmpFileName,
                output_dir=out_path
            )
            print(f"=======  extractorResults : {extractorResults}")
            pass

        ## 이미지 업로드
        # print(f"WorkerMessageHandler :: RunningState :: ExtractProc :: {processName} :: image up {jobProtocol.file_path} ")

        from common_lib.Utils.S3PathUtil import S3PathUtil
        S3Utils.UploadFolder( minioConnection=  s3Connection, local_dir=out_path , s3_dir= S3PathUtil.Dir(f"{s3NormalDir}/{sub_path}"))

        ## tmp extractor 이하 폴더 삭제
        FileUtils.Rm(out_path)

        ## 마커 변경

        from Defines.Defines import Defines
        messageChannelSet = self._parentProcess.GetEventBus().GetMessageChannel(Defines.E_IPC.MAKE_SET)

        jobMarkProtocol = messageChannelSet.Get(jobProtocol.file_path)
        print(f"WorkerMessageHandler :: RunningState :: {jobMarkProtocol.file_path} {jobMarkProtocol.job_state}" )

        jobMarkProtocol.SetComplete()
        messageChannelSet.Set(jobProtocol.file_path , jobMarkProtocol )

        pass

    def Proc(self):


        while not self._jobQueue.IsEmpty():
            jobProtocol = self._jobQueue.Pop()
            if jobProtocol == None:
                break

            self.ExtractProc(jobProtocol)

            time.sleep(0.2)
        # print(f"RunningState::Proc")
        pass

    pass
