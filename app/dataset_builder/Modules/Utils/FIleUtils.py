






class FileUtils:

    @staticmethod
    def MkDir( mkdir_path ):
        from pathlib import Path
        path = Path(mkdir_path)
        path.mkdir(parents=True, exist_ok=True)



    def Rm( rm_path ):
        from pathlib import Path
        import shutil

        path = Path(rm_path)

        if not path.exists():
            return

        if path.is_file() or path.is_symlink():
            path.unlink()  # 파일 삭제
        elif path.is_dir():
            shutil.rmtree(path)  # 폴더 전체 삭제

    pass