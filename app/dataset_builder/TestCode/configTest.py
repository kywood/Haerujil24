import sys
from pathlib import Path

def main():
    # 프로젝트/패키지 import를 위해 루트 추가 (필요하다면)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # TestCode의 상위 = dataset_builder

    from common_lib.Config.ConfigLoader import ConfigLoader

    base_dir = Path(__file__).resolve().parents[1]   # dataset_builder
    config_path = base_dir / "config.ini"            # dataset_builder/config.ini

    ConfigLoader.instance(path=str(config_path))

def main2():
    a=Path(__file__).resolve()
    # print(a)

    print(Path(__file__).resolve())

    print(Path(__file__).resolve().parents[1])

    pass

if __name__ == "__main__":
    main2()
