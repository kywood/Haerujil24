from Modules.App.BuilerApp import BuilderApp
from Modules.DataSetBuilder import DataSetBuilder


def main():
    from common_lib.Path.BasePath import BasePath
    from common_lib.Config.ConfigLoader import ConfigLoader
    from Defines.Defines import Defines


    config_file = BasePath.instance().File(Defines.CONFIG_FILE_NAME)
    configLoader = ConfigLoader.instance(config_file)

    app = BuilderApp(
        basePath=BasePath.instance(),
        configLoader=configLoader
    )

    app.Run()

    #
    # app = DataSetBuilder(BasePath.instance() ,configLoader )
    #
    # app.Start()


    pass


if __name__ == '__main__':
    main()