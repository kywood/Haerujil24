



def main():
    from common_lib.ObjectStorage.ObjectStorageConnection import MinioConnection
    con=MinioConnection(
        endpoint="http://127.0.0.1:9000",
        bucket="haerujil-unnormal-row",
        access_key="oracle",
        region_name="us-east-1",
        secret_access_key="oracleoracle"
    )

    with con.con() as session :
        storage = session.storage("haerujil-unnormal-row")

        for k in storage.ls():
            print(k)

        # 또는
        lists = list(storage.ls())
        print(lists)
        # lists = storage.ls()
        #
        # o=10


    pass

if __name__ == '__main__':
    main()