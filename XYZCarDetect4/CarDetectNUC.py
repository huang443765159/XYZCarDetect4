from XYZNetwork3.Utils.CONST import CONST
from XYZNetwork3.MixSERVER import MixSERVER
from XYZNetwork3.MixINVITER import MixINVITER

from XYZCarDetect4.Utils.Signals import Signals
from XYZCarDetect4.Utils.CODEC import CODEC, decode


class CarDetectNUC:

    def __init__(self):
        self._network = MixSERVER(tcp_port=CODEC.TCP.PORT, event_cb=self._event_cd, recv_cb=self._recv)
        self._inviter = MixINVITER()
        self._inviter.set_machine_sn(machine_sn=CODEC.TCP.MACHINE_SN)
        self._inviter.add_network(network=self._network)
        self._was_stopped = False
        # SIGNAL
        self.sign = Signals()

    def _event_cd(self, module: str, code: str, value: tuple):
        self.__event(module_name='CAR_DETECT', module=module, code=code, value=value)

    def _event_tv(self, module: str, code: str, value: tuple):
        self.__event(module_name='TV', module=module, code=code, value=value)

    def __event(self, module_name: str, module: str, code: str, value: tuple):
        if module == CONST.PROTOCOL.TCP and code == CONST.EVENT.CONNECTION:
            is_online, (ip, port) = value
            print(f'{module_name} TCP IS ONLINE={ip, port, is_online}')

    # 接收到图片后，用信号是车和当前frame图片发送出来
    def _recv(self, data: bytes, ip: str, pkt_id: int):
        head, rx_msg = decode(data=data)
        if head == CODEC.HEAD_TO_NUC:
            self.sign.car_stopped.emit(rx_msg['was_stopped'], rx_msg['frame'], rx_msg['timestamp'])
            self._was_stopped = rx_msg['was_stopped']

    def get_was_stopped(self) -> bool:
        return self._was_stopped

    def exit(self):
        self._network.exit()
        self._inviter.exit()
