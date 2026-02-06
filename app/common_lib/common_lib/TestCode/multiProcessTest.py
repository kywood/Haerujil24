from common_lib.MessageQueue.QueueType import E_QUEUE_TYPE


def main():
    from common_lib.MessageQueue.MpMessageQueue import MpMessageQueue
    from common_lib.MessageQueue.ChannelDTO import ChannelDTO
    from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE

    from common_lib.MessageQueue.ChannelDTO import ChannelQueueQueueDTO
    from common_lib.MessageQueue.ChannelDTO import ChannelQueueHSetDTO
    messageQueue = MpMessageQueue(channel_queue_dtos=[
                                    ChannelQueueQueueDTO(
                                       channel_name="COMQ"
                                    ) ,
                                    ChannelQueueHSetDTO(
                                        channel_name="PQ"
                                    ),
                                ] )

    from common_lib.MessageQueue.IPCS.IPCController import IPCController
    IPCController()
    
    ## TODO 1
    ## 이부분에서 실행을 할시 예외가 터짐

    from common_lib.multiProcess.MultiProcesser import MultiProcesser
    mp = MultiProcesser(messageQueue)

    mp.Init()

    # from common_lib.MessageQueue.ChannelDTO import ChannelDTO
    # from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE

    from common_lib.MessageQueue.MessageHandler import MessageHandler
    from common_lib.TestCode.testProcess import cProducerProcess
    from common_lib.MessageQueue.ChannelDTO import ChannelQueueDTO
    mp.Append(cProducerProcess(messageQueue=messageQueue ,
                               channelDtos=[
                                   ChannelDTO(
                                       channel_name="COMQ",
                                       channel_type=E_CHANNEL_TYPE.SERVER
                                   ) ,
                                   ChannelDTO(
                                       channel_name="PQ",
                                       channel_type=E_CHANNEL_TYPE.NONE
                                   )
                               ] ,
                               messageHandler=MessageHandler()
                               ))
    from common_lib.TestCode.testProcess import cConsumerProcess
    mp.Append(cConsumerProcess(
        name="com1",
        messageQueue=messageQueue,
        channelDtos=[
            ChannelDTO(
                channel_name="COMQ",
                channel_type=E_CHANNEL_TYPE.CLIENT
            ),
            ChannelDTO(
                channel_name="PQ",
                channel_type=E_CHANNEL_TYPE.NONE
            )
        ],
        messageHandler=MessageHandler()
    ))
    mp.Append(cConsumerProcess(
        name="com2",
        messageQueue=messageQueue,
        channelDtos=[
            ChannelDTO(
                channel_name="COMQ",
                channel_type=E_CHANNEL_TYPE.CLIENT
            ),
            ChannelDTO(
                channel_name="PQ",
                channel_type=E_CHANNEL_TYPE.NONE
            )
        ],
        messageHandler=MessageHandler()
    ))
    # mp.Append(cConsumerProcess(
    #     name="com3",
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

#
# def main2():
#
#     while True:
#
#         print("cProducerProcess :: CallProcessing Send >> ")
#         time.sleep(0.2)
#
#         pass
#
#     pass

if __name__ == '__main__':
    main()