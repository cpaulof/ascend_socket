import cv2

class Camera(object):
    def __init__(self, device=0):
        self.device = device
        self._stop_read = False

    def capture(self,):
        cap = cv2.VideoCapture(self.device)
        _, frame = cap.read()
        cap.release()
        return frame

    def read(self):
        cap = cv2.VideoCapture(self.device)
        self._stop_read = False
        while not self._stop_read:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            yield frame
            cv2.waitKey(0)

