


def main():
    from common_lib.Path.BasePath import BasePath
    from common_lib.Config.ConfigLoader import ConfigLoader
    from Defines.Defines import Defines

    config_file = BasePath.instance().GetBasePath()

    # File(Defines.CONFIG_FILE_NAME)

    print(config_file)

    config_file= BasePath.instance().SetUp(1)
    print(config_file)

    config_file = BasePath.instance().File(Defines.CONFIG_FILE_NAME)
    print(config_file)

    ConfigLoader.instance(config_file)

    Defines.FactoryLoader.Factory(Defines.FactoryLoader.E_FACTORY_TYPE.MINIO_FACTORY ,
                                  basePath=BasePath.instance(),
                                  configLoader=ConfigLoader.instance() )

    pass


if __name__ == '__main__':
    main()