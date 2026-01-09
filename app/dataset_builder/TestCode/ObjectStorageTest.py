




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
        from common_lib.Utils.PathUtil import PathUtil
        path = PathUtil.Dir("unnormal")
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

if __name__ == '__main__':
    main()


