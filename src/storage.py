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
        
    def init(self):
        self.spi = spi = SPI(
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


