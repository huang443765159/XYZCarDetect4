import cv2
import threading
import numpy as np
from typing import Optional


class OneCamera:

    def __init__(self):
        self._cap = cv2.VideoCapture(0)
        if self._cap.isOpened():
            self._thread = threading.Thread(target=self._working, daemon=True)
            self._thread_switch = True
            self._thread.start()
        self._cur_frame = None  # type: Optional[None, np.ndarray]

    def _working(self):
        while self._thread_switch:
            ret, frame = self._cap.read()
            if ret:
                self._cur_frame = frame
        self._cap.release()
        cv2.destroyAllWindows()

    def get_cur_frame(self) -> np.ndarray:
        return self._cur_frame

    def stop(self):
        self._thread_switch = False
        self._cap.release()
        cv2.destroyAllWindows()
