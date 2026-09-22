class StateNames:
    IDLE = 0
    INIT = 1
    RECORDING = 2
    PLAYBACK = 3
    ERROR = 4

    NAMES = {
        IDLE: "IDLE",
        INIT: "INIT",
        RECORDING: "RECORDING",
        PLAYBACK: "PLAYBACK",
        ERROR: "ERROR"
    }


class IdleState:
    myName = StateNames.NAMES[StateNames.IDLE]

    def enter(self):
        print("Entering state: " + self.myName)
    
    def run(self):
        print("Running state: " + self.myName)
    
    def exit(self):
        print("Exiting state: " + self.myName)

    
class InitState:
    myName = StateNames.NAMES[StateNames.INIT]

    def __init__(self, controller):
        self.controller = controller
        
    def enter(self):
        print("Entering state: " + self.myName)
    
    def run(self):
        print("Running state: " + self.myName)
        self.controller.nextState = self.controller.states[StateNames.RECORDING]
    
    def exit(self):
        print("Exiting state: " + self.myName)

    
class RecordState:
    myName = StateNames.NAMES[StateNames.RECORDING]
    sMOVING = 0
    sSTATIONARY = 1

    def enter(self):
        print("Entering state: " + self.myName)
    
    def run(self):
        print("Running state: " + self.myName)
    
    def exit(self):
        print("Exiting state: " + self.myName)

    
class PlayState:
    myName = StateNames.NAMES[StateNames.PLAYBACK]

    def enter(self):
        print("Entering state: " + self.myName)
    
    def run(self):
        print("Running state: " + self.myName)
    
    def exit(self):
        print("Exiting state: " + self.myName)

    
class ErrorState:
    myName = StateNames.NAMES[StateNames.ERROR]

    def enter(self):
        print("Entering state: " + self.myName)
    
    def run(self):
        print("Running state: " + self.myName)
    
    def exit(self):
        print("Exiting state: " + self.myName)