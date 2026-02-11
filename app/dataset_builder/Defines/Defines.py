from abc import ABC

from common_lib.Enum.IENUM import IENUM

from Factory.MinioConnectionFactory import MinioConnectionFactory


class IDefine(ABC):

    pass

class Defines(IDefine,ABC):

    CONFIG_FILE_NAME = "config.ini"


    class E_IPC:
        JOB_QUEUE = "JOB_QUEUE"
        MAKE_SET  = "MAKE_SET"


    class ObjectStoragePath:
        bucket="haerujil"
        noraml="normal"
        unnoraml="unnormal"


    class FactoryLoader:

        class E_FACTORY_TYPE(IENUM):
            MINIO_CONNECTION = "MINIO_CONNECTION"

        factories={
            E_FACTORY_TYPE.MINIO_CONNECTION : lambda basePath , configLoader : MinioConnectionFactory.GetConnection( configLoader)
        }

        @staticmethod
        def Factory(factory_type:E_FACTORY_TYPE , *args , **kwargs):
            return Defines.FactoryLoader.factories[factory_type](*args , **kwargs)

    pass



