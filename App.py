from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow


from _example.Gui.Gui import Gui
from _example.Gui.UI.UI import Ui_MainWindow


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._gui = Gui(ui=self._ui)
        QApplication.setStyle('Fusion')

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self._gui.stop()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
