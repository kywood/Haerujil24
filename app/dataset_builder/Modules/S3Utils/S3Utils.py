




class S3Utils:


    @staticmethod
    def GetUnNormalLists(minioConnection):
        with minioConnection.GetStorage() as storage:
            from common_lib.Utils.S3PathUtil import S3PathUtil

            path = S3PathUtil.Dir("unnormal")
            # lists = list(storage.ls(prefix=path))
            lists = list(storage.walk(prefix=path))

            import re
            pattern = re.compile(r'^unnormal/\d{10}/[^/]+$')
            filtered = [x for x in lists if pattern.match(x)]

            # print(lists)

            return filtered
        #
        # from common_lib.Utils.PathUtil import PathUtil
        # path = PathUtil.Dir("unnormal")
        # lists = list(storage.ls(prefix=path))
        # print(lists)
        #
        # return lists



    pass



