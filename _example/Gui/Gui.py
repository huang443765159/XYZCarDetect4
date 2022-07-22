import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox

from _example.Utils import QTools
from _example.Gui.UI.UI import Ui_MainWindow
from _example.Devices.Devices import Devices


class Col:
    DIS = 0
    STATE = 1


class Gui:

    def __init__(self, ui: Ui_MainWindow):
        self._ui = ui
        self._devices = Devices()
        self._detect = self._devices.detect
        # SIGNALS
        self._sign = self._detect.sign  # 因为我们的信号不是Qt信号，所以会出现这种问题
        self._sign.car_stopped.connect(self._signal_is_car)
        self._sign.distance.connect(self._signal_distance)
        # UI
        QTools.table_init(table=self._ui.table_distance, no_edit=False)
        self._ui.table_distance.cellChanged.connect(self._user_input)
        self._ui.btn_debug.stateChanged.connect(self._debug)

    def _signal_is_car(self, is_car: bool, frame: np.array):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        new_frame = cv2.resize(frame, (int(frame.shape[1] * 0.2), int(frame.shape[0] * 0.2)))
        image = QImage(new_frame.data, new_frame.shape[1], new_frame.shape[0], QImage.Format_RGB888)
        self._ui.car_display.setPixmap(QPixmap.fromImage(image))

    def _signal_distance(self, dist_list: list):
        self._ui.table_distance.blockSignals(True)
        for row, one_dis in enumerate(dist_list):
            self._ui.table_distance.item(row, Col.DIS).setText(f'{one_dis}')
            self._ui.table_distance.item(row, Col.STATE).setText('True' if one_dis < 50 else 'False')
            self._ui.table_distance.viewport().update()
        self._ui.table_distance.blockSignals(False)

    def _debug(self, ena: bool):
        self._ui.table_distance.setEditTriggers(QAbstractItemView.CurrentChanged if ena else QAbstractItemView.NoEditTriggers)

    def _user_input(self, row: int, column: int):
        if self._ui.btn_debug.isChecked():
            try:
                if column == Col.DIS:
                    value = int(self._ui.table_distance.item(row, column).text())
                    self._detect.set_dis_list(dis_list=[value] * 3 if value < 3000 else [3000] * 3)
            except ValueError:
                QMessageBox.warning(None, '输入错误', '请输入数字', QMessageBox.Yes)

    def stop(self):
        self._detect.stop()
