import ffmpeg
from pathlib import Path


class ImageExtractorStatic:

    @staticmethod
    def _get_rotation( input_mp4: str) -> int:
        """
        ffprobe로 rotation 메타를 읽어서 -90/90/180/0 등을 반환
        (없으면 0)
        """
        try:
            meta = ffmpeg.probe(input_mp4)
        except ffmpeg.Error:
            return 0

        # video stream 찾기
        streams = meta.get("streams", [])
        v = next((s for s in streams if s.get("codec_type") == "video"), None)
        if not v:
            return 0

        # 1) tags.rotate (가장 흔함)
        rotate = 0
        tags = v.get("tags") or {}
        if "rotate" in tags:
            try:
                rotate = int(tags["rotate"])
            except Exception:
                rotate = 0

        # 2) side_data_list의 displaymatrix 쪽은 ffprobe가 각도 숫자로 안 주는 경우가 많아서
        # tags.rotate가 없으면 0으로 두고 진행 (필요하면 나중에 확장)
        return rotate

    @staticmethod
    def _apply_rotation_filter( stream, rotate: int):
        """
        rotation 값에 따라 transpose/rotate 적용
        """
        r = rotate % 360
        if r == 90:
            # 시계 90
            return stream.filter("transpose", 1)
        if r == 270 or r == -90:
            # 반시계 90 (또는 -90)
            return stream.filter("transpose", 2)
        if r == 180:
            return stream.filter("hflip").filter("vflip")
        return stream  # 0도

    @staticmethod
    def extract_fps(
        input_mp4: str,
        output_dir: str,
        fps: float = 1.0,
        jpg_quality: int = 2,
        overwrite: bool = True,
            quiet: bool = False,
    ) -> int:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        rotate = ImageExtractorStatic._get_rotation(input_mp4)

        stream = ffmpeg.input(input_mp4)
        stream = ImageExtractorStatic._apply_rotation_filter(stream, rotate)

        (
            stream
            .filter("format", "yuvj420p")
            .filter("fps", fps=fps)
            .output(
                str(out_dir / "%06d.jpg"),
                **{"q:v": jpg_quality},
            )
            .run(quiet=quiet, overwrite_output=overwrite)
        )

        return len(list(out_dir.glob("*.jpg")))
