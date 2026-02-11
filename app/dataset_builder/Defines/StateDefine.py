from abc import ABC

from Defines.Defines import IDefine
from Modules.State.StateA import StateA
from Modules.State.StateB import StateB


class StateDefaine(IDefine,ABC):

    class E_STATE:
        STATE_A = "STATE_A"
        STATE_B = "STATE_B"



    pass

class StateMeta:
    metas = {
        StateDefaine.E_STATE.STATE_A : StateA(),
        StateDefaine.E_STATE.STATE_B : StateB()
    }

    pass


class StateFactory:

    @staticmethod
    def CreateStateController():

        

        pass

    pass