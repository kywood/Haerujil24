from App.Dtos.S3Dtos import S3ConnectDtoEx


def main():
    from common_lib.Dtos.S3Dto import S3ConnectDto

    from common_lib.Config.ConfigLoader import ConfigLoader
    config = ConfigLoader.instance( path = "../config.ini")

    s3ConnectDTO = S3ConnectDtoEx().SetDTOFromConfig(
        config
    )

    from common_lib.S3.S3Helper import S3Helper
    S3Helper.fileDownload(

        s3_connect_dto=s3ConnectDTO,
        key="movie_test1.mp4",
        dest_path="../movie_test1.mp4"
    )








    pass



if __name__ == '__main__':
    main()