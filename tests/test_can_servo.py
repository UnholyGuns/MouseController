from rp2350_can import RP2350_CAN
from hitec_registers import Register
import time

try:

    can = RP2350_CAN(rate_kbps="1000KBPS")

except:
    print("failed to start can")

print("CANSTAT:", hex(can.read_byte(0x0E)))
print("CANCTRL:", hex(can.read_byte(0x0F)))

print("CNF1:", hex(can.read_byte(0x2A)))
print("CNF2:", hex(can.read_byte(0x29)))
print("CNF3:", hex(can.read_byte(0x28)))

print("TXB0CTRL before:", hex(can.read_byte(0x30)))

data = [
    ord('r'),
    0x02,
    Register.POSITION
]

can.send(0x000, data)

time.sleep_ms(10)

canintf = can.read_byte(0x2C)
print("CANINTF:", hex(canintf))

if canintf & 0x02:

    RXB1SIDH = 0x71
    RXB1SIDL = 0x72
    RXB1DLC  = 0x75
    RXB1D0   = 0x76

    sid_h = can.read_byte(RXB1SIDH)
    sid_l = can.read_byte(RXB1SIDL)

    can_id = (sid_h << 3) | (sid_l >> 5)

    dlc = can.read_byte(RXB1DLC) & 0x0F

    buf = bytearray(dlc)

    for i in range(dlc):
        buf[i] = can.read_byte(RXB1D0 + i)

    print("CAN ID:", hex(can_id))
    print("DLC:", dlc)
    print("DATA:", [hex(x) for x in buf])

    low  = buf[3]
    high = buf[4]

    position = low | (high << 8)

    print("Position:", position)


# can.send(0x000, data)

# for i in range(20):
#     txctrl = can.read_byte(0x30)
#     print("TXB0CTRL:", hex(txctrl))
#     time.sleep_ms(10)

# time.sleep_ms(100)

# print("TXB0CTRL:", hex(can.read_byte(0x30)))
# print("CANINTF: ", hex(can.read_byte(0x2C)))
# print("EFLG:    ", hex(can.read_byte(0x2D)))

# while True:
#     can.send(0x000, data)

#     for i in range(100):
#         recv_data = can.recv()

#         if recv_data is not None:
#             print("recv:", [hex(i) for i in recv_data])
#             break

#         time.sleep_ms(1)
#     else:
#         print("No data received")

#     time.sleep(1)
