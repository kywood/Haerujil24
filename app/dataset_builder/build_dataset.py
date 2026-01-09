from App.DataSetBuilder import DataSetBuilder


def main():
    from common_lib.Path.BasePath import BasePath
    from common_lib.Config.ConfigLoader import ConfigLoader
    from Defines.Defines import Defines


    config_file = BasePath.instance().File(Defines.CONFIG_FILE_NAME)
    ConfigLoader.instance(config_file)

    app = DataSetBuilder(BasePath.instance() ,ConfigLoader.instance() )

    app.Start()

    pass


if __name__ == '__main__':
    main()