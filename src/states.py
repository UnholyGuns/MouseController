import time

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

        try:
            self.controller.storage.init()

        except Exception as e:
            print("Initialization failed:", e)
            self.controller.nextState = StateNames.ERROR

        print("Initialization Sucessfull!")

        
    
    def run(self):
        print("Running state: " + self.myName)
        self.controller.nextState = StateNames.RECORDING


    
    def exit(self):
        print("Exiting state: " + self.myName)

    
class RecordState:
    myName = StateNames.NAMES[StateNames.RECORDING]

    RECORD_START_DELAY = 3
    SAMPLE_PERIOD_MS = 20

    def __init__(self, controller):
        self.controller = controller
        self.lastRecordTime = time.ticks_ms()
        self.recordingStarted = False
        self.recordStartTime = 0


    def enter(self):
        self.recordStartTime = time.ticks_add(time.ticks_ms(), self.RECORD_START_DELAY*1000)
        self.recordingStarted = False
        print(f"Recording starts in {self.RECORD_START_DELAY} seconds...")

        try:
            self.controller.storage.startRecording()

        except Exception as e:
            print("Could not open recording file during record state:", e)
            self.controller.nextState = StateNames.ERROR


    
    def run(self):
        if not self.recordingStarted:
            if time.ticks_diff(time.ticks_ms(), self.recordStartTime) >= 0:
                self.recordingStarted = True
                print("RECORDING")

            return

        now = time.ticks_ms()

        if time.ticks_diff(now, self.lastRecordTime) >= self.SAMPLE_PERIOD_MS:
            self.lastRecordTime = now

            try:
                posX = self.servoX.getLocation()
                posY = self.servoY.getLocation()
                self.controller.storage.storeValue(posX, posY)

            except Exception as e:
                print("Could not store recording file during record state:", e)
                self.controller.nextState = self.controller.StateNames.ERROR


        
    def exit(self):
        print("Closing the recording and removing last 3 seconds of data")
        self.recordingStarted = False

        try:
            self.controller.storage.stopRecording()

        except Exception as e:
            print("Could not close recording file during record state:", e)
            self.controller.nextState = StateNames.ERROR


    
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
        time.sleep(1)
    
    def exit(self):
        print("Exiting state: " + self.myName)