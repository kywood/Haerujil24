from common_lib.CallBack.CallBack import Func
from common_lib.MessageQueue.IPCS.IPC import IPC
from common_lib.MessageQueue.MessageChannel import MessageChannelQueue, MessageChannelHSet


class MessageQueueDef:



    class MessageChannelFactoryMeta:


        callbacks={
            IPC.E_IPC_TYPE.QUEUE : Func( lambda ipc ,channel_name, channel_type: MessageChannelQueue(ipc ,channel_name, channel_type) ) ,
            IPC.E_IPC_TYPE.HSET  : Func( lambda ipc, channel_name, channel_type: MessageChannelHSet(ipc, channel_name, channel_type))
        }

        @staticmethod
        def FactoryMethod( ipc_type : IPC.E_IPC_TYPE ):
            try:
                return MessageQueueDef.MessageChannelFactoryMeta.callbacks[ipc_type]
            except KeyError as e:
                raise ValueError(f"Unsupported ipc_type: {ipc_type}") from e
