from contextlib import closing

import boto3

from common_lib.Dtos.S3Dto import S3ConnectDto

class S3Helper:


    @staticmethod
    def fileDownload( s3_connect_dto : S3ConnectDto , key: str, dest_path: str):

        with closing(
                boto3.client(
                    "s3",
                    endpoint_url=s3_connect_dto.s3_endpoint,
                    aws_access_key_id=s3_connect_dto.access_key,
                    aws_secret_access_key=s3_connect_dto.secret_access_key,
                    region_name=s3_connect_dto.region_name,
                )
        ) as s3:
            import os
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            s3.download_file( s3_connect_dto.bucket, key, dest_path)

