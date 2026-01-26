from common_lib.Config.ConfigLoader import ConfigLoader
from common_lib.Path.BasePath import BasePath

from App.NormalThread import NormalThread


class DataSetBuilder:


    def __init__(self ,
                 basePath : BasePath ,
                 configLoader : ConfigLoader
                 ):


        self._basePath = basePath
        self._configLoader = configLoader


        from common_lib.Thread.ThreadController import ThreadController
        self._threadController = ThreadController()

        self._threadController.append(
            NormalThread(self._threadController)
        )

        from Defines.Defines import Defines
        minioConnection = Defines.FactoryLoader.Factory(Defines.FactoryLoader.E_FACTORY_TYPE.MINIO_CONNECTION,
                                      basePath=BasePath.instance(),
                                      configLoader=ConfigLoader.instance())


        bucket_name = Defines.ObjectStoragePath.bucket

        with minioConnection.con() as session :
            storage = session.storage(bucket_name)

            from common_lib.Utils.PathUtil import PathUtil

            path = PathUtil.Dir(Defines.ObjectStoragePath.unnoraml)



            # path = PathUtil.file("train2017")
            # 또는
            lists = list(storage.ls(prefix=path))
            print("================= lists =============")
            print(lists)
            print("================= lists =============")

            ## list 를 구해서
            ##  안에 들어가서

            lists = list(storage.walk(prefix=path))
            print("================= walks =============")
            print(lists)
            print("================= walks =============")

            from App.ObjectStorageUtils.ObjectStorageUtils import ObjectStorageUtils
            for key in ObjectStorageUtils.GetFileName(storage,path , suffix="mp4"):
                print(key)

            # print(ll)

            print("==============================")

            rr=ObjectStorageUtils.GetFileName(storage, path, suffix="mp4")

            rrlists = list(rr)

            print(rrlists)





        pass

    def Start(self):
        self._threadController.Start()
        pass


