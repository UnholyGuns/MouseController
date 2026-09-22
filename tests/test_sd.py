from machine import Pin, SPI
import os
import sdcard

print("Starting SD test")

spi = SPI(
    0,
    baudrate=1_000_000,
    polarity=0,
    phase=0,
    sck=Pin(2),
    mosi=Pin(3),
    miso=Pin(4)
)

cs = Pin(5, Pin.OUT, value=1)

print("SPI initialized")

sd = sdcard.SDCard(spi, cs)

print("SD card initialized")

vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")

print("SD mounted")
print("Files:", os.listdir("/sd"))

print("Writing test file...")

f = open("/sd/test.txt", "w")
f.write("Hello from the RP2350!\n")
f.write("SD card is working.\n")
f.close()

print("Reading test file...")

f = open("/sd/test.txt", "r")
print(f.read())
f.close()

print("Files:", os.listdir("/sd"))