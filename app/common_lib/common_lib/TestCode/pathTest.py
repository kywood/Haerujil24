

def main():
    from common_lib.Path.BasePath import BasePath
    pa=BasePath.instance().GetBasePath()

    print(pa)

    d = BasePath.instance().Dir("a", "bb", "aa")

    print(d)

    d = BasePath.instance().File("a", "bb", "aa", "a.mov")
    print(d)

    pass


if __name__ == '__main__':
    main()