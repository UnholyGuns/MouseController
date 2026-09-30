from machine import Pin, SPI #exposes hardware
import os #deals with the micro python filesystem abstraction, allows mounting, listdir, ...
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

with open("/sd/test.txt", "w+") as f:
    print("test file opened, writing 1 tuple")
    f.write("1,1\n")
    f.write("1,1\n")
    print(f.tell())
    f.seek(2)
    data = f.read(5)
    print(f"data at position 2: {data}")
    print(dir(f))
    print(dir(os))

print("fin")