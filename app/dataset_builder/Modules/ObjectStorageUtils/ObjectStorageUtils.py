from collections.abc import Iterable

from common_lib.ObjectStorage.ObjectStorage import ObjectStorage


class ObjectStorageUtils:




    @staticmethod
    def GetFileName(storage:ObjectStorage , path , suffix)-> Iterable[str]:
        # lists = list(storage.walk(prefix=path))
        for key in storage.walk(prefix=path):
            if key.endswith(suffix):
                yield key

        #
        # return [
        #     key for key in storage.walk(prefix=path)
        #     if key.endswith(suffix)
        # ]

        # return lists
