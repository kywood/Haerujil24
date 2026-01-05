import ffmpeg
from pathlib import Path


def extract_fps(input_mp4: str, output_dir: str, fps: float = 1.0):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    (
        ffmpeg
        .input(input_mp4)
        # 폰 영상 회전 메타 반영
        .filter("transpose", 2)  # ✅ -90도 보정(일단 고정)
        # 안정적인 픽셀 포맷으로 변환(인코더 에러 방지)
        .filter("format", "yuvj420p")
        .filter("fps", fps=fps)
        .output(
            str(output_dir / "%06d.jpg"),
            **{"q:v": 2}  # ✅ qscale 경고 제거
        )
        .run(quiet=False, overwrite_output=True)
    )

    print(f"[DONE] <><><>< extracted {len(list(output_dir.glob('*.jpg')))} frames")


if __name__ == "__main__":
    extract_fps("/data/input.mp4", "/out", fps=1.0)
