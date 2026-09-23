from states import *
from storage import Storage

class MouseController:
    def __init__(self):
        self.storage = Storage()

        self.states = {
            StateNames.IDLE: IdleState(),
            StateNames.INIT: InitState(self), 
            StateNames.RECORDING: RecordState(self),
            StateNames.PLAYBACK: PlayState(),
            StateNames.ERROR: ErrorState()
        }
        self.currentState = StateNames.IDLE
        self.nextState = None

    def begin(self):
        self.nextState = StateNames.INIT

    def transitionTo(self, newstate: StateNames):
        self.states[self.currentState].exit()
        self.currentState = newstate
        self.states[self.currentState].enter()
        
    def run(self):
        if self.nextState != self.currentState:
            self.transitionTo(self.nextState)
        else:
            self.states[self.currentState].run()
    
    def printState(self):
        print("Current state: " + self.states[self.currentState].myName)
