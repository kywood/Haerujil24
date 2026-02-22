from pathlib import Path
from Modules.Extrator.ImageExtractor import ImageExtractor


def main():
    # 로컬 테스트 mp4 (프로젝트 루트에 있다고 했으니)
    input_mp4 = Path("/data/input.mp4").resolve()
    if not input_mp4.exists():
        raise FileNotFoundError(f"mp4 not found: {input_mp4}")

    # 출력 폴더
    out_dir = Path("/out").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    extractor = ImageExtractor(quiet=False)

    # 1) FPS 테스트 (무조건 프레임 나오는지 검증용)
    count = extractor.extract_fps(
        input_mp4=str(input_mp4),
        output_dir=str(out_dir),
        fps=1.0,
        jpg_quality=2,
        overwrite=True,
    )
    print(f"[OK] ============ FPS extracted frames: {count} -> {out_dir}")

    # 2) (원하면) Scene 테스트
    # scene_dir = Path("../frames_scene").resolve()
    # scene_dir.mkdir(parents=True, exist_ok=True)
    # scene_count = extractor.extract_scene(
    #     input_mp4=str(input_mp4),
    #     output_dir=str(scene_dir),
    #     scene_thr=0.15,
    #     overwrite=True,
    # )
    # print(f"[OK] Scene extracted frames: {scene_count} -> {scene_dir}")


if __name__ == "__main__":
    main()
