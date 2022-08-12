import time
import pickle
import datetime

from XYZUtil4.tools.for_class import singleton


def get_timestamp() -> int:
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_array = time.strptime(cur_time, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(time_array)
    return int(timestamp)


def encode(head, **kwargs) -> bytes:
    return pickle.dumps((head, kwargs))


def decode(data: bytes) -> tuple:
    head, rx_msg = pickle.loads(data)
    return head, rx_msg


class _Tcp:
    PORT = 10888
    MACHINE_SN = 'XYZCarDetect4'


class _Mcu:
    IP = '192.168.50.130'
    PORT = 54188


class _State:
    DIS1 = 800
    DIS2 = 900
    DIS3 = 1000


@singleton
class _Codec:
    TCP = _Tcp()
    MUC = _Mcu()
    STATE = _State()
    HEAD_TO_MCU = b'\xe4'
    HEAD_TO_NUC = b'\xe5'


CODEC = _Codec()
