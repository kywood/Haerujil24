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


    def _Download(self ,s3Connection , s3FilePath , localTmpFilePath ):

        S3Utils.DownloadFile(s3Connection ,s3FilePath , localTmpFilePath )



    def _TransForm(self ,localOutDirPath,  s3FilePath ):

        import sys
        from pathlib import Path

        if sys.platform == "win32":
            from PIL import Image
            img = Image.new("RGB", (1, 1), color="black")
            # Path(out_path) / "000001.jpg"
            img.save(Path(localOutDirPath) / "000001.jpg")
            img.save(Path(localOutDirPath) / "000002.jpg")
            img.save(Path(localOutDirPath) / "000003.jpg")
            pass
        else:
            from Modules.Extrator.ImageExtractorStatic import ImageExtractorStatic
            extractorResults = ImageExtractorStatic.extract_fps(
                input_mp4=s3FilePath,
                output_dir=localOutDirPath
            )
            print(f"=======  extractorResults : {extractorResults}")
            pass

    def _Marking(self, jobProtocol):
        from Defines.Defines import Defines
        messageChannelSet = self._parentProcess.GetEventBus().GetMessageChannel(Defines.E_IPC.MAKE_SET)

        jobMarkProtocol = messageChannelSet.Get(jobProtocol.file_path)
        print(f"WorkerMessageHandler :: RunningState :: {jobMarkProtocol.file_path} {jobMarkProtocol.job_state}" )

        jobMarkProtocol.SetComplete()
        messageChannelSet.Set(jobProtocol.file_path , jobMarkProtocol )

        pass

    def ExtractProc(self , jobProtocol ):

        ## ENV

        print(f"WorkerMessageHandler :: RunningState :: ExtractProc :: {self._parentProcess.GetName()} :: image down and extract {jobProtocol.file_path} ")

        configLoader = self._parentProcess.GetConfigLoader()

        from Factory.MinioConnectionFactory import MinioConnectionFactory
        from pathlib import Path
        from Modules.Extrator.ExtractorUtils import ExtractorUtils


        tmpDirName = self._parentProcess.GetTmpDir()
        s3Connection = MinioConnectionFactory.GetConnection( configLoader )
        tmpFileName = Path( tmpDirName ) /  jobProtocol.file_path
        extractorPrefix = ExtractorUtils.GetExtractorPrefix( configLoader )
        s3NormalDir = ExtractorUtils.GetS3NormalDirName(configLoader)


        src = Path(jobProtocol.file_path)
        # 첫 폴더 제거 후 새 루트로 붙이기
        sub_path = Path(*src.parts[1:-1])  # ('2026010900')
        out_path = Path(tmpDirName) / extractorPrefix / sub_path

        self._Download(s3Connection=s3Connection , s3FilePath=jobProtocol.file_path , localTmpFilePath=tmpFileName)

        from Modules.Utils.FIleUtils import FileUtils
        FileUtils.MkDir( out_path )

        ## 이미지 변환
        self._TransForm(localOutDirPath=out_path , s3FilePath=tmpFileName )

        ## 이미지 업로드
        from common_lib.Utils.S3PathUtil import S3PathUtil
        S3Utils.UploadFolder( minioConnection=  s3Connection, local_dir=out_path , s3_dir= S3PathUtil.Dir(f"{s3NormalDir}/{sub_path}"))

        ## tmp extractor 이하 폴더 삭제
        FileUtils.Rm(out_path)

        ## 마커 변경
        self._Marking(jobProtocol)


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
