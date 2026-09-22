from states import *
from storage import Storage

class MouseController:
    def __init__(self):
        self.storage = Storage()

        self.states = {
            StateNames.IDLE: IdleState(),
            StateNames.INIT: InitState(self), #pass reference to the controller so we can access function in the controller
            StateNames.RECORDING: RecordState(),
            StateNames.PLAYBACK: PlayState(),
            StateNames.ERROR: ErrorState()
        }
        self.currentState = self.states[StateNames.IDLE]
        self.nextState = None

    def begin(self):
        self.nextState = self.states[StateNames.IDLE]

    def transitionTo(self, newstate: StateNames):
        self.currentState.exit()
        self.currentState = self.states[newstate]
        self.currentState.enter()
        
    def run(self):
        if self.nextState != self.currentState:
            self.transitionTo(self.nextState)
        else:
            self.currentState.run()
    
    def printState(self):
        print("Current state: " + self.currentState.myName)
