import multiprocessing

from common_lib.multiProcess.MultiProcesser import MultiProcesser


def main():
    from common_lib.MessageQueue.MpMessageQueue import MpMessageQueue
    #
    # from multiprocessing import Queue
    # qs = {"COMQ": Queue() ,
    #       "COMQ_IN": Queue() ,
    #       "COMQ_OUT": Queue(),
    #       }
    # from multiprocessing import Lock
    # locks = {"COMQ": Lock() ,
    #          "COMQ_IN": Lock(),
    #          "COMQ_OUT": Lock(),
    #          }

    # qs = multiprocessing.Manager().dict()
    # locks = multiprocessing.Manager().dict()

    from common_lib.MessageQueue.ChannelDTO import ChannelDTO
    from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE



    messageQueue = MpMessageQueue(channel_dtos=[
                                   ChannelDTO(
                                       channel_name="COMQ",
                                       channel_type=E_CHANNEL_TYPE.SERVER
                                   )
                               ] )


    mp = MultiProcesser(messageQueue)

    mp.Init()

    # from common_lib.MessageQueue.ChannelDTO import ChannelDTO
    # from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE

    from common_lib.multiProcess.abProcess import cProducerProcess
    from common_lib.MessageQueue.MessageHandler import MessageHandler
    mp.Append(cProducerProcess(messageQueue=messageQueue ,
                               channelDtos=[
                                   ChannelDTO(
                                       channel_name="COMQ",
                                       channel_type=E_CHANNEL_TYPE.SERVER
                                   )
                               ] ,
                               messageHandler=MessageHandler()
                               ))
    from common_lib.multiProcess.abProcess import cConsumerProcess


    mp.Append(cConsumerProcess(
        messageQueue=messageQueue,
        channelDtos=[
            ChannelDTO(
                channel_name="COMQ",
                channel_type=E_CHANNEL_TYPE.CLIENT
            )
        ],
        messageHandler=MessageHandler()
    ))
    # mp.Append(cConsumerProcess(
    #     messageQueue=messageQueue,
    #     channelDtos=[
    #         ChannelDTO(
    #             channel_name="COMQ",
    #             channel_type=E_CHANNEL_TYPE.CLIENT
    #         )
    #     ],
    #     messageHandler=MessageHandler()
    # ))
    # mp.Append(cConsumerProcess(
    #     messageQueue=messageQueue,
    #     channelDtos=[
    #         ChannelDTO(
    #             channel_name="COMQ",
    #             channel_type=E_CHANNEL_TYPE.CLIENT
    #         )
    #     ],
    #     messageHandler=MessageHandler()
    # ))

    mp.Start()


    pass


if __name__ == '__main__':
    main()