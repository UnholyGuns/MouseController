from machine import Pin, SPI #exposes hardware
import os #deals with the micro python filesystem abstraction, allows mounting, listdir, ...
import sdcard

SD_SCK_PIN = 2
SD_MOSI_PIN = 3
SD_MISO_PIN = 4
SD_CSN_PIN = 5

class Storage:
    def __init__(self):       
        self.spi = None
        self.cs = None
        self.sd = None
        self.vfs = None

        self.recordingPath = "/sd/BRUH.txt"
        self.recordFile = None


    def init(self):
        self.spi = SPI(
            0,
            baudrate=1_000_000,
            polarity=0,
            phase=0,
            sck=Pin(SD_SCK_PIN),
            mosi=Pin(SD_MOSI_PIN),
            miso=Pin(SD_MISO_PIN)
        )

        self.cs = Pin(SD_CSN_PIN, Pin.OUT, value=1)
        self.sd = sdcard.SDCard(self.spi, self.cs)
        self.vfs = os.VfsFat(self.sd)
        os.mount(self.vfs, "/sd")

        # Lets do a test file read write to verify
        testData = "lemmiegetuhhhh"

        try:
            with open(self.recordingPath, "w") as f:
                f.write(testData)

            with open(self.recordingPath, "r") as f:
                readData = f.read()

            if readData != testData:
                raise RuntimeError("SD read/write verification failed")

        finally:
            os.remove(self.recordingPath)



    def startRecording(self):
        self.recordFile = open(self.recordingPath, "w")



    def startReading(self):
        self.recordFile = open(self.recordingPath, "r")



    def closeFile(self):
        self.recordFile.close()
        self.recordFile = None



    def storeValue(self, posX: int, posY: int):
        self.recordFile.write(f"{posX},{posY}\n")



    def getValues(self):
        line = self.recordFile.readline()

        if line == "":# handle End of file
            self.recordFile.seek(0)
            line = self.recordFile.readline()

        line = line.strip()
        parts = line.split(",")
        posX = int(parts[0])
        posY = int(parts[1])

        return posX, posY





