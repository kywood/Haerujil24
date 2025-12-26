from fastapi import FastAPI
from Controller.IController import IController

class ServingServer:
    def __init__(self, title: str = "Haerujil24 Serving"):
        self.app = FastAPI(title=title)
        self._controllers: list[IController] = []

    def add_controller(self, controller: IController) -> "ServingServer":
        self._controllers.append(controller)
        return self

    def build(self) -> FastAPI:
        for c in self._controllers:
            c.register(self.app)
        return self.app
#
#
# def InitializeSingleton():
#
#
#     pass


def create_app() -> FastAPI:
    from Controller.ServingController import ServingController
    from Config.ConfigLoader import ConfigLoader

    from Inference.InferenceManager import InferenceManager

    config = ConfigLoader.instance()
    InferenceManager.instance(config).Initialize()


    server = ServingServer(title=config.get('APP','NAME'))
    server.add_controller(ServingController(config))
    app = server.build()
    return app


app = create_app()


def main():
    import os
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    workers = int(os.getenv("WORKERS", "1"))  # GPU 서빙이면 1 권장

    uvicorn.run(
        app,
        host=host,
        port=port,
        workers=workers,
        reload=False,
        log_level="info",
    )


if __name__ == '__main__':
    main()