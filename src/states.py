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
        pass
    
    def exit(self):
        pass

    
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
            return

        print("Initialization Sucessfull!")

        
    
    def run(self):
        print("Running state: " + self.myName)
        self.controller.nextState = StateNames.IDLE


    
    def exit(self):
        print("Exiting state: " + self.myName)


    
class RecordState:
    myName = StateNames.NAMES[StateNames.RECORDING]

    SAMPLE_PERIOD_MS = 1000

    def __init__(self, controller):
        self.controller = controller
        self.lastRecordTime = time.ticks_ms()

    def enter(self):
        print("Begin recording...")
        try:
            self.controller.storage.startRecording()

        except Exception as e:
            print("Could not open recording file during record state:", e)
            self.controller.nextState = StateNames.ERROR


    
    def run(self):
        now = time.ticks_ms()

        if time.ticks_diff(now, self.lastRecordTime) >= self.SAMPLE_PERIOD_MS:
            self.lastRecordTime = now

            try:
                posX = self.controller.servoX.getLocation()
                posY = self.controller.servoY.getLocation()
                self.controller.storage.storeValue(posX, posY)

            except Exception as e:
                print("Could not store recording file during record state:", e)
                self.controller.nextState = StateNames.ERROR


        
    def exit(self):
        try:
            self.controller.storage.closeFile()

        except Exception as e:
            print("Could not close recording file during record state:", e)
            self.controller.nextState = StateNames.ERROR


    
class PlayState:
    myName = StateNames.NAMES[StateNames.PLAYBACK]

    SAMPLE_PERIOD_MS = 1000



    def __init__(self, controller):
        self.controller = controller
        self.lastRecordTime = time.ticks_ms()



    def enter(self):
        try:
            self.controller.storage.startReading()

        except Exception as e:
            print("Could not open recording file during playback state:", e)
            self.controller.nextState = StateNames.ERROR


    
    def run(self):
        now = time.ticks_ms()

        if time.ticks_diff(now, self.lastRecordTime) >= self.SAMPLE_PERIOD_MS:
            self.lastRecordTime = now

            try:
                posX, posY = self.controller.storage.getValues()
                print(f"X: {posX}, Y: {posY}")

            except Exception as e:
                print("Could not retreive data playback state:", e)
                self.controller.nextState = StateNames.ERROR


        
    def exit(self):
        print("Ending playback")

        try:
            self.controller.storage.closeFile()

        except Exception as e:
            print("Could not close recording file during record state:", e)
            self.controller.nextState = StateNames.ERROR



    
class ErrorState:
    myName = StateNames.NAMES[StateNames.ERROR]

    def enter(self):
        print("Entering state: " + self.myName)
    
    def run(self):
        print("Running state: " + self.myName)
        time.sleep(1)
    
    def exit(self):
        print("Exiting state: " + self.myName)