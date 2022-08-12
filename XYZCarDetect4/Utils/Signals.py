from XYZUtil4.customclass.Signal import Signal
from XYZUtil4.tools.for_class import singleton


@singleton
class Signals:

    distance = Signal(list)  # dis_list
    car_stopped = Signal(bool, int)  # was_stopped, timestamp
