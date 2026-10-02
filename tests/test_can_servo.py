from rp2350_can import RP2350_CAN
from hitec_registers import Register
import time


SERVO_ID = 0x02
CAN_ID = 0x000


try:
    can = RP2350_CAN(rate_kbps="1000KBPS")
except Exception as e:
    print("Failed to start CAN:", e)
    raise


def read_register(register):
    # Send Hitec register read
    data = [
        ord('r'),
        SERVO_ID,
        register
    ]

    can.send(CAN_ID, data)

    # Wait up to ~20 ms for the response
    for i in range(20):

        message = can.recv()

        if message is not None:
            can_id, recv_data = message

            # Make sure this is the response we're expecting
            if (
                len(recv_data) >= 5
                and recv_data[0] == ord('v')
                and recv_data[1] == SERVO_ID
                and recv_data[2] == register
            ):
                low = recv_data[3]
                high = recv_data[4]

                return low | (high << 8)

        time.sleep_ms(1)

    return None

print("REF_1 after reboot:", hex(read_register(0xA6)))

# Set Start Motor Free
ref1 = read_register(0xA6)
new_ref1 = ref1 | 0x0002

can.send(CAN_ID, [
    ord('x'),
    SERVO_ID,
    0xA6,
    new_ref1 & 0xFF,
    (new_ref1 >> 8) & 0xFF
])

time.sleep_ms(100)

print("REF_1 before save:", hex(read_register(0xA6)))


# Save configuration
can.send(CAN_ID, [
    ord('x'),
    SERVO_ID,
    0x70,
    0xFF,
    0xFF
])

# Get acknowledgement
for i in range(100):
    message = can.recv()
    if message is not None:
        can_id, data = message
        print("SAVE response:", [hex(x) for x in data])
        break
    time.sleep_ms(1)


# IMPORTANT: give flash save plenty of time
print("Waiting for flash save...")
time.sleep_ms(2000)

print("REF_1 after save:", hex(read_register(0xA6)))
print("Now power-cycle the servo.")

# # Read existing REF_1 first
# ref1 = read_register(0xA6)

# print("REF_1 before:", hex(ref1))

# if ref1 is None:
#     raise RuntimeError("Could not read REF_1")


# # Preserve every existing bit, set only Start Motor Free (bit 1)
# new_ref1 = ref1 | (1 << 1)

# print("Writing REF_1:", hex(new_ref1))


# # Hitec write-and-read command
# command = [
#     ord('x'),
#     SERVO_ID,
#     0xA6,
#     new_ref1 & 0xFF,          # low byte
#     (new_ref1 >> 8) & 0xFF   # high byte
# ]

# can.send(CAN_ID, command)

# time.sleep_ms(20)

# message = can.recv()

# if message is not None:
#     can_id, data = message

#     print("Write response ID:", hex(can_id))
#     print("Write response:", [hex(x) for x in data])
# else:
#     print("No response to write")


# # Read it back independently
# time.sleep_ms(20)

# ref1_after = read_register(0xA6)

# print("REF_1 after:", hex(ref1_after))

# --------------------------------------------------
# Put servo into EMG FREE
# POWER = 0x0200
# --------------------------------------------------

# free_command = [
#     ord('x'),
#     SERVO_ID,
#     Register.POWER,
#     0x00,
#     0x02
# ]

# print("Setting servo to FREE...")
# can.send(CAN_ID, free_command)

# time.sleep_ms(20)

# message = can.recv()

# if message is not None:
#     can_id, data = message

#     print("Response ID:", hex(can_id))
#     print("Response:", [hex(x) for x in data])
# else:
#     print("No response to FREE command")


# # Read the braking register
# setup = read_register(0xA2)

# print("SETUP:", hex(setup))

# print("Brake instead of Free:", (setup >> 2) & 1)
# print("Over Volt Brake:      ", (setup >> 3) & 1)

# brake_voltage = read_register(0x80)

# print("Overvolt brake raw:", brake_voltage)

# if brake_voltage is not None:
#     print("Overvolt threshold:", brake_voltage / 100.0, "V")

# ref1 = read_register(0xA6)

# print("REF_1:", hex(ref1) if ref1 is not None else None)

# if ref1 is not None:
#     print("Start Motor Free supported:    ", (ref1 >> 1) & 1)
#     print("Fail Safe Motor Free supported:", (ref1 >> 2) & 1)

# # Read the braking register
# version = read_register(Register.PRODUCT_VER_0)

# print("Version:", version)

# # --------------------------------------------------
# # Monitor position, torque and current
# # --------------------------------------------------

# print()
# print("Servo is FREE.")
# print("Move the servo by hand...")
# print()

# while True:

#     position = read_register(Register.POSITION)
#     torque   = read_register(Register.TORQUE)
#     current  = read_register(Register.CURRENT)
#     voltage = read_register(Register.VOLTAGE)

#     print(
#         "Position:", position,
#         " Torque:", torque,
#         " Current:", current, "mA",
#         " Voltage:", voltage / 100.0, "V"
#     )

#     time.sleep_ms(100)



# from rp2350_can import RP2350_CAN
# from hitec_registers import Register
# import time


# try:
#     can = RP2350_CAN(rate_kbps="1000KBPS")
# except Exception as e:
#     print("Failed to start CAN:", e)
#     raise


# # Hitec: read POSITION from servo ID1 = 2
# data = [
#     ord('r'),
#     0x02,
#     Register.POSITION
# ]

# print("Sending:", [hex(x) for x in data])

# can.send(0x000, data)


# # Give the servo up to ~100 ms to respond
# for i in range(100):

#     message = can.recv()

#     if message is not None:
#         can_id, recv_data = message

#         print("CAN ID:", hex(can_id))
#         print("DATA:", [hex(x) for x in recv_data])

#         # Expected Hitec response:
#         # 'v', servo ID, register, low byte, high byte
#         if len(recv_data) >= 5:
#             low  = recv_data[3]
#             high = recv_data[4]

#             position = low | (high << 8)

#             print("Position:", position)

#         break

#     time.sleep_ms(1)

# else:
#     print("No data received")