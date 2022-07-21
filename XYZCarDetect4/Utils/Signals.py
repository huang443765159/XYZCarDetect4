import numpy as np

from XYZUtil4.customclass.Signal import Signal
from XYZUtil4.tools.for_class import singleton


@singleton
class Signals:

    distance = Signal(list)  # dis_list
    is_car = Signal(bool, np.array, int)  # is_car, frame, timestamp
