


def main():

    from pathlib import Path
    print(Path(__file__).resolve())

    print(Path(__file__).resolve().parents[0])

    pass


def main2():
    from common_lib.Path.BasePath import BasePath
    pa=BasePath.instance().GetBasePath()

    print(pa)

    d= BasePath.instance().Dir("a","bb","aa")

    print(d)

    d = BasePath.instance().File("a", "bb", "aa","a.mov")
    print(d)

    import sys
    entry = sys.argv[0]

    print(entry)

    from pathlib import Path
    p = Path(entry)

    base = p.resolve().parent

    print(base)

    pass



if __name__ == '__main__':
    main2()