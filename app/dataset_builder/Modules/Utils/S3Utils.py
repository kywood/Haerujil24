




class S3Utils:


    @staticmethod
    def GetUnNormalLists(minioConnection , unnormal_dir :str = "unnormal"):
        with minioConnection.GetStorage() as storage:
            from common_lib.Utils.S3PathUtil import S3PathUtil

            path = S3PathUtil.Dir(unnormal_dir)
            # lists = list(storage.ls(prefix=path))
            lists = list(storage.walk(prefix=path))

            import re

            prefix = re.escape(unnormal_dir.strip("/"))
            pattern = re.compile(rf'^{prefix}/\d{{10}}/[^/]+$')
            # pattern = re.compile(r'^unnormal/\d{10}/[^/]+$')
            filtered = [x for x in lists if pattern.match(x)]

            # print(lists)

            return filtered

    @staticmethod
    def DownloadFile(minioConnection , s3_file_path , local_file_path):
        with minioConnection.GetStorage() as storage:
            storage.get(key=s3_file_path, local_path=local_file_path)

    @staticmethod
    def UploadFolder(minioConnection, local_dir, s3_dir):
        from pathlib import Path

        local_root = Path(local_dir)
        if not local_root.exists():
            raise FileNotFoundError(f"Local dir not found: {local_root}")
        if not local_root.is_dir():
            raise ValueError(f"Not a directory: {local_root}")

        s3_dir = (s3_dir or "").strip("/")

        items = []

        # 🔥 핵심: local_root 기준 상대경로 유지
        for file_path in local_root.rglob("*"):
            if not file_path.is_file():
                continue

            rel_path = file_path.relative_to(local_root).as_posix()
            # 예: 2026010900/000001.jpg

            key = f"{s3_dir}/{rel_path}" if s3_dir else rel_path

            items.append((str(file_path), key))

        if not items:
            return

        with minioConnection.GetStorage() as storage:
            storage.puts(items)

    @staticmethod
    def UploadFile(minioConnection, local_path, s3_dir):
        from pathlib import Path

        lp = Path(local_path)
        if not lp.exists():
            raise FileNotFoundError(f"Local file not found: {lp}")
        if not lp.is_file():
            raise ValueError(f"Not a file: {lp}")

        s3_dir = (s3_dir or "").strip("/")
        key = f"{s3_dir}/{lp.name}" if s3_dir else lp.name

        with minioConnection.GetStorage() as storage:
            storage.puts([(str(lp), key)])

    @staticmethod
    def DeleteFolder(minioConnection, s3_dir):
        """
        s3_dir 하위 모든 객체 삭제
        """
        s3_dir = (s3_dir or "").strip("/")

        with minioConnection.GetStorage() as storage:
            # prefix 기준으로 객체 목록 조회
            objects = storage.list(prefix=s3_dir, recursive=True)

            keys = []
            for obj in objects:
                keys.append(obj.object_name)

            if not keys:
                return

            for k in keys:
                # 삭제
                storage.remove(k)


    @staticmethod
    def DeleteFile(minioConnection, s3_file_path):
        """
        단일 객체 삭제
        """
        s3_key = (s3_file_path or "").strip("/")

        if not s3_key:
            return

        with minioConnection.GetStorage() as storage:
            storage.delete(s3_key)

