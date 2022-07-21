import struct
from typing import List

from XYZUtil4.network.UDP import UDP
from XYZNetwork3.Utils.CONST import CONST
from XYZNetwork3.MixCLIENT import MixCLIENT

from ._OneCamera import OneCamera
from .Utils.Signals import Signals
from .Utils.CODEC import CODEC, encode, get_timestamp


class CarDetect:

    def __init__(self):
        # SIGNAL
        self.sign = Signals()
        self._camera = OneCamera()
        self._udp = UDP(is_nuc=True)
        self._udp.set_peer_address(address=(CODEC.MUC.IP, CODEC.MUC.PORT))
        self._udp.sign_recv.connect(self._signal_udp_recv)
        self._dis_list = list()  # type: List[int]
        self._was_display = False
        # NETWORK
        self._network = MixCLIENT(tcp_port=CODEC.TCP.PORT, event_cb=self._event)
        self._network.set_machine_sn(machine_sn=CODEC.TCP.MACHINE_SN)

    def _signal_udp_recv(self, data: bytes, ip: str, port: int):
        if data[0: 1] == CODEC.HEAD_TO_MCU:
            dis_list = list(struct.unpack('!hhh', data[2: 8]))
            self.set_dis_list(dis_list=dis_list)

    def _event(self, module: str, code: str, value: tuple):
        if module == CONST.PROTOCOL.TCP and code == CONST.EVENT.CONNECTION:
            is_online, (ip, port) = value
            print(f'TCP ONLINE={ip, port, is_online}')

    def set_dis_list(self, dis_list: list):  # 边缘出发
        self.sign.distance.emit(dis_list)
        if dis_list[0] > CODEC.STATE.DIS1:
            self._was_display = False
        if self._was_display:
            return
        if dis_list[0] < CODEC.STATE.DIS1 and dis_list[1] < CODEC.STATE.DIS2 and dis_list[2] < CODEC.STATE.DIS3:
            cur_frame = self._camera.get_cur_frame()
            self.sign.is_car.emit(True, cur_frame)
            self._was_display = True
            if self._network.tcp.is_connected():
                tx_msg = encode(head=CODEC.HEAD_TO_NUC, is_car=True, frame=cur_frame, timestamp=get_timestamp())
                self._network.tcp.send(data=tx_msg)

    def get_dis_list(self) -> list:
        return self._dis_list

    def stop(self):
        self._camera.stop()
