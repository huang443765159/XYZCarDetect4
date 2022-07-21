import sys
from PyQt5.QtCore import QCoreApplication, QObject

from XYZCarDetect4.CarDetectNUC import CarDetectNUC


class Nuc(QObject):

    def __init__(self):
        super(Nuc, self).__init__()
        self._nuc = CarDetectNUC()


if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    nuc = Nuc()
    sys.exit(app.exec_())
