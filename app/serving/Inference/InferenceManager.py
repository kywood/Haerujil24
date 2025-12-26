from Utils.Singleton import SingletonBase


class InferenceManager(SingletonBase):

    def __init__(self , config):
        SingletonBase.__init__(self)
        self._config = config


        self._model = None
        self._device = "auto"
        self._initialized = False

        from Dtos.S3Dto import S3ConnectDto

        self.s3ConnectDTO = S3ConnectDto().SetDTOFromConfig(
            self._config
        )

        self._init()

        pass

    def _init(self):
        self._checkCachDir()

    def Initialize(self):
        """
        모델 파일 다운로드 + 모델 로딩까지 보장
        """
        if self._initialized:
            return True

        # 모델 파일 보장
        self._downloadModel()
        # 모델 로딩
        self._loadModel()

        self._initialized = True
        return True


    def _checkCachDir(self):
        ## 해당 결로가 있으면 말고 없다면 생성함
        from Config.ConfigHelper import ConfigHelper
        from Utils.FileUtils import FileUtils

        cachePath = ConfigHelper.GetCachePath()
        FileUtils.CheckDirAndMake(cachePath)



        pass

    def DownloadModel(self):
        self._downloadModel()

        pass

    def _downloadModel(self):
        from Config.ConfigHelper import ConfigHelper
        from S3.S3Helper import S3Helper

        remodeModelPath = ConfigHelper.GetModelRemotePath()
        localModelPath = ConfigHelper.GetLocalCachePath()

        print(f"remodeModelPath : {remodeModelPath} localModelPath:{localModelPath} ")

        try:
            S3Helper.fileDownload(
                s3_connect_dto=self.s3ConnectDTO,
                key=remodeModelPath,
                dest_path=localModelPath
            )
            return True
        except Exception as e:
            raise e


    def _loadModel(self):
        """
        YOLO / torch 모델 로딩
        """
        from ultralytics import YOLO
        import torch

        if self._model is not None:
            return

        # device 자동 선택
        if self._device == "auto":
            self._device = "cuda" if torch.cuda.is_available() else "cpu"

        from Config.ConfigHelper import ConfigHelper
        localModelPath = ConfigHelper.GetLocalCachePath()

        print(
            f"[InferenceManager] Loading model: {localModelPath} "
            f"(device={self._device})"
        )
        # print("[InferenceManager] torch.cuda.is_available():", torch.cuda.is_available())
        # print("[InferenceManager] model param device:", next(self._model.model.parameters()).device)

        self._model = YOLO(str(localModelPath))

        try:
            self._model.to(self._device)
            print(f"[InferenceManager] model.to({self._device}) OK")
        except RuntimeError as e:
            print("[InferenceManager] model.to(device) FAILED:", e)
            print("[InferenceManager][ERROR] model.to(device) RuntimeError:", e)

            if self._device.startswith("cuda"):
                print("[InferenceManager] Fallback to CPU")
                self._device = "cpu"
                self._model.to("cpu")
            else:
                raise  # CPU도 실패면 서버 띄울 이유 없음
        except Exception as e:
            # 🔥 예상 못한 에러
            print("[InferenceManager][FATAL] model.to(device) failed:", e)
            raise  # 이건 숨기면 안 됨

        print("[InferenceManager] torch.cuda.is_available():", torch.cuda.is_available())
        print("[InferenceManager] model param device:", next(self._model.model.parameters()).device)

        pass

    def infer(self, image):
        """
        image:
          - 파일 경로 (str)
          - PIL.Image
          - numpy.ndarray
        """

        if not self._initialized:
            self.Initialize()

        return self._model(image, device=self._device)
    #
    # def Println(self):
    #
    #     pass


    pass

# #
# config=10
# #
# InferenceModelManager.instance(config=config)
#
# InferenceModelManager.instance().Println()
# # # InferenceModelManager(config=config)
# #

