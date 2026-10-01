"""
Python port of HITEC's public CAN servo register header.

Source:
    hitec-can-servo-reg-public.h
    HITEC CAN Servo Register Header file
    Date: 2023-04-18
    Version: 2.0

Original copyright:
    Copyright 2017-2023 HITEC RCD Korea, INC.

The original header states that it is distributed under the BSD license and
warns that reserved values must not be changed.

Port notes:
- C enum values are represented as class attributes.
- C #define bit positions are represented as integer constants.
- Macros that depended on an external reg_val()/getbit() implementation are
  represented as pure helper functions taking the register value explicitly.
- No CAN transport behavior is implemented here. This module is only the
  register/bit definition layer.
"""


class Register:
    PRODUCT_NO_0 = 0x00
    PRODUCT_VER_0 = 0x02
    # 0x04 reserved
    STATUS = 0x06
    FUNC_LIST = 0x08
    # 0x0A reserved
    POSITION = 0x0C
    VELOCITY = 0x0E
    TORQUE = 0x10
    VOLTAGE = 0x12
    TEMPER = 0x14
    CURRENT = 0x16
    TURN_COUNT = 0x18
    POSITION_32BITS = 0x1A
    POSITION_32BITS_H = 0x1C
    POSITION_NEW = 0x1E
    TMP_CONFIG = 0x20
    # 0x22 reserved
    TURN_NEW = 0x24
    SPEC_TORQUE = 0x26
    # 0x28, 0x2A reserved
    UNITLESS_RAD_MODE = 0x2C
    STREAM_TIME = 0x2E
    STREAM_MODE = 0x30
    ID1 = 0x32
    # 0x34, 0x36 reserved
    CAN_BAUDRATE = 0x38
    STREAM_ID_H = 0x3A
    ID2_H = 0x3C
    ID2_L = 0x3E
    SAMPLE_POINT = 0x40
    STREAM_ID_L = 0x42
    SERVO_MODE = 0x44
    POWER = 0x46
    EMERGENCY_STOP = 0x48
    PARAM_VERSION_1 = 0x4A
    PARAM_VERSION_2 = 0x4C
    DEADBAND = 0x4E
    POS_MAX = 0x50
    POS_MIN = 0x52
    VELOCITY_MAX = 0x54
    TORQUE_MAX = 0x56
    VOLTAGE_MAX = 0x58
    VOLTAGE_MIN = 0x5A
    TEMPER_MAX = 0x5C
    PRODUCT_INFO = 0x5E
    # 0x60 system reserved
    MOTOR_PWM_MINIMUM = 0x62
    INERTIA_RANGE = 0x64
    INERTIA_CONF = 0x66
    PEAK_POWER_RATE = 0x68
    CAN_MODE = 0x6A
    TEMPER_MIN = 0x6C
    FACTORY_DEFAULT = 0x6E
    CONFIG_SAVE = 0x70
    CONFIG_LOCK = 0x72
    PRODUCT_NO = 0x74
    PRODUCT_VER = 0x76
    PARAM_VER = 0x78
    STARTUP_POSITION_NEW = 0x7A
    VOLT_R_H = 0x7C
    VOLT_R_L = 0x7E
    BRAKE_VOLT = 0x80
    BRAKE_TIME = 0x82
    SETUP_4 = 0x84
    MOTOR_PWM_PERIOD = 0x86
    MOTOR_PWM_DEADTIME = 0x88
    P_GAIN = 0x8A
    D_GAIN = 0x8C
    I_GAIN = 0x8E
    C_GAIN = 0x90
    ACC = 0x92
    FAIL_SAFE_POSITION_NEW = 0x94
    # 0x96 not present in original enum
    POS_LOCK_LIMIT = 0x98
    POS_LOCK_TIME = 0x9A
    POS_LOCK_TORQUE_RATIO = 0x9C
    # 0x9E reserved; 0xA0 system settings/reserved
    SETUP_1 = 0xA2
    PID_TIME = 0xA4
    REF_1 = 0xA6
    PAD_VOLT = 0xA8
    # 0xAA, 0xAC reserved
    ZERO_OFFSET = 0xAE
    POSITION_MAX = 0xB0
    POSITION_MIN = 0xB2
    FAIL_SAFE_TIME = 0xB4
    CURRENT_VALUE_ADC_0 = 0xB6
    CURRENT_VALUE_ADC_4095 = 0xB8
    # 0xBA, 0xBC system reserved
    MOTOR_PSC = 0xBE
    # 0xC0 product reserved
    POSITION_MID = 0xC2
    CURRENT_K2 = 0xC4
    ECHO = 0xC6
    TIME_L = 0xC8
    TIME_H = 0xCA
    USER_1 = 0xCC
    USER_2 = 0xCE
    MOTOR_TEMP = 0xD0
    MOTOR_TEMP_C = 0xD1
    TEMP = 0xD2
    HUM = 0xD4
    CURRENT_K = 0xD6
    CURRENT_MAX = 0xD8
    SPEED_VOLTAGE = 0xDA
    SPEED_UP = 0xDC
    SPEED_DN = 0xDE
    SPEED_ES = 0xE0
    STREAM_0 = 0xE2
    STREAM_1 = 0xE4
    STREAM_2 = 0xE6
    STREAM_3 = 0xE8


class StatusBit:
    ENABLED = 0
    OVER_CURRENT = 1
    OVER_LOADED = 2


class FunctionBit:
    ENABLE = 0
    EDIT_TURN_COUNT = 1
    I_GAIN_X1000 = 2
    OVERVOLT_BRAKE = 3
    OVERVOLT_BRAKE_TIME = 4
    SELECT_PAD = 5
    VOLTAGE_PEAK = 6
    FAST_VOLTAGE = 7
    WIDE_VOLTAGE = 8
    CURRENT_CUT = 9
    OVERLOADED = 10
    STREAM_CAN_ID = 11


class TmpConfigBit:
    PAUSE_STREAM = 0


class Setup4Bit:
    # 0=CW, 1=CCW. Servo reset needed. FW >= 2.0.
    MOTOR_DIRECTION = 0


class Setup1Bit:
    SELECT_PAD = 0
    STARTUP_POSITION_NEW = 1
    USE_BRAKE_INSTEAD_FREE = 2
    USE_HIGH_VOLTAGE_BRAKE = 3
    USE_WIDE_VOLTAGE = 5
    USE_CURRENT_CUT = 6
    USE_STREAM_CAN_ID = 7
    USE_VOLTAGE_MIN_REAL_TIME = 8
    USE_SPEED_UP_OR_DN_AS_REVERSE = 9
    USE_FAIL_SAFE_POSITION = 10
    USE_2PHASE_BRAKE = 11
    USE_ID_REALTIME = 12
    USE_RETURN_CAN_ID_OR_1 = 13


class EmergencyMode:
    # Values stored in POWER bits 10:9.
    NORMAL = 0
    FREE = 1          # register bits = 0x0200
    SPEED_DOWN = 2    # register bits = 0x0400
    HOLD = 3          # register bits = 0x0600


def emergency_mode(power_register_value):
    """Equivalent to the original EMG_MODE() macro."""
    return (power_register_value >> 9) & 0x03


def brake_mode(setup1_register_value):
    """Equivalent to the original BRAKE_MODE() macro."""
    return (setup1_register_value >> Setup1Bit.USE_BRAKE_INSTEAD_FREE) & 0x01


def velocity_conv(velocity, pid_time):
    """
    Python equivalent of the original VelocityConv(V, PT) macro.

    Original:
        ((PT) * 60 * 16384 / 360 / (V) / 10 / 10)
    """
    return pid_time * 60 * 16384 / 360 / velocity / 10 / 10
