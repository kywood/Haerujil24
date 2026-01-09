
import hashlib
from contextlib import AsyncExitStack
from pathlib import Path


def md5_string(text: str, encoding: str = "utf-8") -> str:
    """문자열의 MD5 해시(hex)"""
    return hashlib.md5(text.encode(encoding)).hexdigest()



def main():
    p= md5_string("korea12345324343434ㅈㅇㅈㅇㅈㅇㅈㅇㅈ34")

    print(p)

    "eb8f1714b5b66e32412d6794ddb2726d"
    "305289b27f53da00adeee847265f50ff"
    "2022be45d7bc24bd07d28bb55d91c7de"

    ## 암호화  AES-128 , AES-512  https->AES-2048
    #
    # MD5
    # AES
    # zip
    #
    #
    #
    # C  -> S
    #
    # korea -> hash
    # korea 암호화  ->  0x872bhsudbncux  hash -> zip -> ijwd28 전송
    #
    # S
    # ijwd28 -> 0x872bhsudbncux hash    korea1

    ## API Server 사용자가 로긴이 됐는지 어케 확인 하나??

    ## DB mongo db
    ## mongo respository
    ## mysql -> 확장이 어렵다. replicaset



    ## mongo sharding ( 확장 ) + replicaset ( 복제 ) >>>>
    ## 스케일 인   ( 컴퓨터 업그레이드 )
    ## 스케일 아웃 ( 컴퓨터 더 구입 )


    pass


if __name__ == '__main__':
    main()