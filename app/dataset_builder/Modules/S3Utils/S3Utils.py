




class S3Utils:


    @staticmethod
    def GetUnNormalLists(minioConnection):
        with minioConnection.GetStorage() as storage:
            from common_lib.Utils.PathUtil import PathUtil

            path = PathUtil.Dir("unnormal")
            lists = list(storage.ls(prefix=path))
            print(lists)

            return lists
        #
        # from common_lib.Utils.PathUtil import PathUtil
        # path = PathUtil.Dir("unnormal")
        # lists = list(storage.ls(prefix=path))
        # print(lists)
        #
        # return lists



    pass



