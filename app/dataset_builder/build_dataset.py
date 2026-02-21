import time

from Modules.App.BuilerApp import BuilderApp
# from Modules.DataSetBuilder import DataSetBuilder
#


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



if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method("spawn", force=True)

    main()