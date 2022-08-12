import struct
from typing import List

from XYZUtil4.network.UDP import UDP

# from ._OneCamera import OneCamera
from .Utils.Signals import Signals
from .Utils.CODEC import CODEC, get_timestamp


class CarDetect:

    def __init__(self):
        # SIGNAL
        self.sign = Signals()
        # self._camera = OneCamera()
        self._udp = UDP(is_nuc=True)
        self._udp.set_peer_address(address=(CODEC.MUC.IP, CODEC.MUC.PORT))
        self._udp.sign_recv.connect(self._signal_udp_recv)
        self._dis_list = list()  # type: List[int]
        self._was_stopped = False

    def _signal_udp_recv(self, data: bytes, ip: str, port: int):
        if data[0: 1] == CODEC.HEAD_TO_MCU:
            dis_list = list(struct.unpack('!hhh', data[2: 8]))
            self.set_dis_list(dis_list=dis_list)

    def set_dis_list(self, dis_list: list):  # 边缘出发
        was_stopped = False
        self.sign.distance.emit(dis_list)
        if dis_list[0] > CODEC.STATE.DIS1 and dis_list[1] > CODEC.STATE.DIS2 and dis_list[2] > CODEC.STATE.DIS3:
            was_stopped = False
        elif dis_list[0] < CODEC.STATE.DIS1 and dis_list[1] < CODEC.STATE.DIS2 and dis_list[2] < CODEC.STATE.DIS3:
            was_stopped = True
        if self._was_stopped != was_stopped:
            self._was_stopped = was_stopped
            # cur_frame = self._camera.get_cur_frame()
            # self.sign.car_stopped.emit(self._was_stopped, cur_frame, get_timestamp())
            self.sign.car_stopped.emit(self._was_stopped, get_timestamp())

    def get_dis_list(self) -> list:
        return self._dis_list

    def get_car_stopped(self) -> bool:
        return self._was_stopped

    def stop(self):
        pass
        # self._camera.stop()
