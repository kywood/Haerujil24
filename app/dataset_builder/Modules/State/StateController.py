



class StateController:

    def __init__(self):


        self._container = {}
        pass

    def AppendState(self , state):
        self._container[ state.GetStateID() ] = state

    pass