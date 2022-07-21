from XYZUtil4.tools.for_class import singleton

from XYZCarDetect4.CarDetect import CarDetect


@singleton
class Devices:

    def __init__(self):
        self.detect = CarDetect()
