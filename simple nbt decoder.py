from enum import Enum
import gzip
import struct
from typing import Tuple


class NbtType(Enum):
    END = 0x00
    BYTE = 0x01
    SHORT = 0x02
    INT = 0x03
    LONG = 0x04
    FLOAT = 0x05
    DOUBLE = 0x06
    BYTE_ARRAY = 0x07
    STRING = 0x08
    LIST = 0x09
    COMPOUND = 0x0a
    INT_ARRAY = 0x0b
    LONG_ARRAY = 0x0c


def read_nbt(f):
    decoded_data = {}

    while True:
        data_type = f.read(1)
        # End tag
        if data_type == NbtType.END:
            return decoded_data

        name_length_bytes = f.read(2)
        name_length = int.from_bytes(name_length_bytes, "big")
        name_bytes = f.read(name_length)
        name = name_bytes.decode("utf-8")

        match data_type:
            case NbtType.BYTE:
                data = f.read(1)
            case NbtType.SHORT:
                data = int.from_bytes(f.read(2), "big", signed=True)
            case NbtType.INT:
                data = int.from_bytes(f.read(4), "big", signed=True)
            case NbtType.LONG:
                data = int.from_bytes(f.read(8), "big", signed=True)
            case NbtType.FLOAT:
                data = struct.unpack(">f", f.read(4))
            case NbtType.DOUBLE:
                data = struct.unpack(">d", f.read(8))
            case NbtType.BYTE_ARRAY:
                array_length = int.from_bytes(f.read(4), "big")
                data = f.read(array_length)
            case NbtType.STRING:
                string_length = int.from_bytes(f.read(2), "big")
                data = f.read(string_length).decode("utf-8")
            case NbtType.LIST:
                pass
            case NbtType.COMPOUND:
                pass
            case NbtType.INT_ARRAY:
                array_length = int.from_bytes(f.read(4), "big")
                data = []
                for byte in range(array_length):
                    element = int.from_bytes(f.read(4), "big", signed=True)
                    data.append(element)
            case NbtType.LONG_ARRAY:
                array_length = int.from_bytes(f.read(4), "big")
                data = []
                for byte in range(array_length):
                    element = int.from_bytes(f.read(8), "big", signed=True)
                    data.append(element)
            case _:
                raise ValueError(f"Expected datatype byte to be in range of 0x00-0x0c, got {data_type}")

        decoded_data[name] = data


nbt_f = gzip.open("player_data.dat", "rb")
read_nbt(nbt_f)
