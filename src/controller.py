from states import *

class MouseController:
    def __init__(self):
        self.states = {
            StateNames.IDLE: IdleState(),
            StateNames.INIT: InitState(),
            StateNames.RECORDING: RecordState(),
            StateNames.PLAYBACK: PlayState(),
            StateNames.ERROR: ErrorState()
        }
        self.currentState = self.states[StateNames.IDLE]
        
    def transitionTo(self, newstate: StateNames):
        self.currentState.exit()
        self.currentState = self.states[newstate]
        self.currentState.enter()
        
    def run(self):
        self.currentState.run()
    
    def printState(self):
        print("Current state: " + self.currentState.myName)
        