from common_lib.multiProcess.abProcess import cTestProcess


def main():

    process = cTestProcess()


    IP = "10.156.133.122"
    PORT = 11157
    PASSWORD = 'Odyssey2!'
    QueueNM = "testQ"

    redisPools = cRedisStaticPool().Init(
        host = IP,
        port = PORT,
        pass_word = PASSWORD
    )
    redis = redisPools.GetRedisRap()
    messageQueue = cRedisMessageQueue(radis)

    eventBus = cEventBus(process, messageQueue)
    process.SetEventBus(eventBus)

    ## consumer

    # eventBus.CreateMessageChannel("JOBQ", E_CHANNEL_TYPE.SERVER)
    # eventBus.CreateMessageChannel("COMQ", E_CHANNEL_TYPE.CLIENT)

    eventBus.CreateMessageChannel("JOBQ", E_CHANNEL_TYPE.SERVER)
    eventBus.CreateMessageChannel("COMQ", E_CHANNEL_TYPE.SERVER)
    # eventBus.CreateMessageChannel("P1", E_CHANNEL_TYPE.SERVER)

    from ody_lib.message_queue.cMessageHandler import cMessageHandler
    messageHandler = cMessageHandler()

    channelJobq = eventBus.GetChannel("JOBQ")
    channelComq = eventBus.GetChannel("COMQ")
    # channelP1 = eventBus.GetChannel("P1")

    eventBus.AddListener(cEventListener().AppendChannels([channelJobq, channelComq]).SetMessageHandler(messageHandler))
    eventBus.Start()

    pass


if __name__ == '__main__':
    main()