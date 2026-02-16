

def main():
    from common_lib.MessageQueue.MpMessageQueue import MpMessageQueue
    from common_lib.MessageQueue.ChannelDTO import ChannelDTO
    from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE


    messageQueue = MpMessageQueue(channel_dtos=[
                                   ChannelDTO(
                                       channel_name="COMQ",
                                       channel_type=E_CHANNEL_TYPE.NONE
                                   )
                               ] )

    from common_lib.multiProcess.MultiProcesser import MultiProcesser
    mp = MultiProcesser(messageQueue)

    mp.Init()

    # from common_lib.MessageQueue.ChannelDTO import ChannelDTO
    # from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE

    from common_lib.MessageQueue.MessageHandler import MessageHandler
    from common_lib.TestCode.testProcess import cProducerProcess
    mp.Append(cProducerProcess(messageQueue=messageQueue ,
                               channelDtos=[
                                   ChannelDTO(
                                       channel_name="COMQ",
                                       channel_type=E_CHANNEL_TYPE.SERVER
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
            )
        ],
        messageHandler=MessageHandler()
    ))
    mp.Append(cConsumerProcess(
        name="com3",
        messageQueue=messageQueue,
        channelDtos=[
            ChannelDTO(
                channel_name="COMQ",
                channel_type=E_CHANNEL_TYPE.CLIENT
            )
        ],
        messageHandler=MessageHandler()
    ))

    mp.Start()


    pass

#
# def main2():
#
#     while True:
#
#         print("cProducerProcess :: ProcProcessing Send >> ")
#         time.sleep(0.2)
#
#         pass
#
#     pass

if __name__ == '__main__':
    main()