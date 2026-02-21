import sys

from common_lib.Utils.Singleton import SingletonBase


class BasePath(SingletonBase):


    def __init__(self , relative_path: str = None ):
        super().__init__()
        from pathlib import Path

        # entry = sys.argv[0]
        # base_path = Path(entry).resolve().parent

        import os
        base_path = Path(os.getcwd()).resolve()
        #
        if relative_path:
            base_path = (base_path / relative_path).resolve()

        self._basePath = base_path

        # self._basePath = Path(__file__).resolve().parents[0]
        pass

    def GetBasePath(self):
        return self._basePath
    #
    #
    # def GetBBPath(self):
    #     import os
    #     from pathlib import Path
    #     base_path = Path(os.getcwd()).resolve()
    #
    #
    #     return base_path


    # def GetBasePath(self,up: int = 0):
    #     if up <= 0:
    #         return self._basePath
    #
    #     cur = self._basePath
    #     for _ in range(up):
    #         parent = cur.parent
    #         if parent == cur:
    #             break
    #         cur = parent
    #     return cur

    def SetUp(self, n: int = 1):
        """
        basePath = basePath.parents[n-1]
        """
        cur = self._basePath
        for _ in range(n):
            parent = cur.parent
            if parent == cur:
                break
            cur = parent

        self._basePath = cur
        return self._basePath

    def SetBasePath(self, path):
        from pathlib import Path
        self._basePath = Path(path).expanduser().resolve()
        return self._basePath

    # def Path(self ,*paths: str, trailing_slash = False ):
    #     new_paths = (self._basePath.as_posix(), *paths)
    #     from common_lib.Utils.S3PathUtil import S3PathUtil
    #     return S3PathUtil.Path(*new_paths,
    #                            trailing_slash=trailing_slash)

    def Path(self, *paths: str, trailing_slash: bool = False) -> str:
        p = self._basePath.joinpath(*paths)
        # resolve()는 존재하지 않는 경로에 대해 OS/환경에 따라 불편할 수 있어 선택 사항
        # p = p.resolve()
        s = p.as_posix()
        if trailing_slash and not s.endswith("/"):
            s += "/"
        return s


    def Dir(self, *paths: str) -> str:
        # 디렉토리 문자열 용도면 trailing slash 붙이는게 편하면 True로
        return self.Path(*paths, trailing_slash=True)

    def File(self, *paths: str) -> str:
        # 파일 경로는 trailing slash 없어야 정상
        return self.Path(*paths, trailing_slash=False)
    #
    # def Dir(self ,*paths: str ):
    #     new_paths = (self._basePath.as_posix(), *paths)
    #     from common_lib.Utils.S3PathUtil import S3PathUtil
    #     return S3PathUtil.Dir(*new_paths)
    #
    # def File(self ,*paths: str ):
    #     new_paths = (self._basePath.as_posix(), *paths)
    #     from common_lib.Utils.S3PathUtil import S3PathUtil
    #     return S3PathUtil.File(*new_paths)
#

# #
# #
# if __name__ == '__main__':
#     pa=BasePath.instance("../../").GetBasePath()
#
#     print(pa)
#
#     d= BasePath.instance().Dir("a","bb","aa")
#
#     print(d)
#
#     d = BasePath.instance().File("a", "bb", "aa","a.mov")
#     print(d)
#




