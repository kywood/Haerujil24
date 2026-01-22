

def main():
    from common_lib.multiProcess.abProcess import cTestProcess
    process = cTestProcess()

    from common_lib.MessageQueue.EventBus import EventBus
    from common_lib.MessageQueue.MpMessageQueue import MpMessageQueue

    messageQueue = MpMessageQueue()

    eventBus = EventBus(process, messageQueue)
    process.SetEventBus(eventBus)

    from common_lib.MessageQueue.ChannelType import E_CHANNEL_TYPE
    from common_lib.MessageQueue.MessageHandler import MessageHandler
    from common_lib.MessageQueue.EventListener import EventListener

    channelJobq = eventBus.CreateMessageChannel("JOBQ", E_CHANNEL_TYPE.SERVER)
    channelComq = eventBus.CreateMessageChannel("COMQ", E_CHANNEL_TYPE.SERVER)

    messageHandler = MessageHandler()

    # channelJobq = eventBus.GetChannel("JOBQ")
    # channelComq = eventBus.GetChannel("COMQ")

    eventBus.AddListener(EventListener().AppendChannels([channelJobq, channelComq]).SetMessageHandler(messageHandler))
    eventBus.Start()
    pass


if __name__ == '__main__':

    main()