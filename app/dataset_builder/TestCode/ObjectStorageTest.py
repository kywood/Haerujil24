




def main():
    from common_lib.ObjectStorage.ObjectStorageConnection import MinioConnection
    con=MinioConnection(
        endpoint="http://127.0.0.1:9000",
        user_name="oracle",
        password="oracleoracle",
        region_name="us-east-1"
    )

    bucket_name= "haerujil"

    with con.con() as session :
        storage = session.storage(bucket_name)
        #
        # for k in storage.ls():
        #     print(k)
        #
        #
        from common_lib.Utils.S3PathUtil import S3PathUtil
        path = S3PathUtil.Dir("unnormal")
        # path = PathUtil.file("train2017")
        # 또는
        lists = list(storage.ls(prefix=path))
        print(lists)

        lists = list(storage.walk(prefix=path))
        print(lists)

        # path = PathUtil.file("train2017", "000000000009.jpg")
        #
        # lists = storage.stat(key=path)
        # print(lists)
        #
        # lists = storage.exists(key=path)
        # print(lists)
        #
        # lists = storage.delete(key=path)
        # print(lists)
        #
        # path = PathUtil.dir("normal")
        # storage.mkdir(key=path)

        #
        # path = PathUtil.dir("train2017","korea")
        # storage.delete(key=path)

    pass

def main2():
    from Factory.MinioConnectionFactory import MinioConnectionFactory

    from common_lib.Path.BasePath import BasePath
    from Defines.Defines import Defines
    config_file = BasePath.instance("../").File(Defines.CONFIG_FILE_NAME)
    from common_lib.Config.ConfigLoader import ConfigLoader
    configLoader = ConfigLoader.instance(config_file)

    minioConnection = MinioConnectionFactory.GetConnection(
        configLoader
    )

    with minioConnection.GetSession() as session :
        bucket_name = "haerujil"

        storage = session.storage(bucket_name)

        lists=storage.ls()

        for li in lists:
            print(li)

        # print(lists)


        pass


    pass


def main3():
    from common_lib.Path.BasePath import BasePath
    from Defines.Defines import Defines
    config_file = BasePath.instance("../").File(Defines.CONFIG_FILE_NAME)
    from common_lib.Config.ConfigLoader import ConfigLoader
    configLoader = ConfigLoader.instance(config_file)

    from Factory.MinioConnectionFactory import MinioConnectionFactory
    minioConnection = MinioConnectionFactory.GetConnection(
        configLoader
    )


    with minioConnection.GetStorage() as storage :

        lists = storage.ls()
        for li in lists:
            print(li)

        # print(lists)



def main4():
    from common_lib.Path.BasePath import BasePath
    from Defines.Defines import Defines
    config_file = BasePath.instance("../").File(Defines.CONFIG_FILE_NAME)
    from common_lib.Config.ConfigLoader import ConfigLoader
    configLoader = ConfigLoader.instance(config_file)

    from Factory.MinioConnectionFactory import MinioConnectionFactory
    minioConnection = MinioConnectionFactory.GetConnection(
        configLoader
    )

    from Modules.S3Utils.S3Utils import S3Utils
    ret=S3Utils.GetUnNormalLists(minioConnection)


    print(ret)

    pass

if __name__ == '__main__':
    main4()


