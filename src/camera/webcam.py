import cv2

class Webcam:
    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)
        if not self.cap.isOpened():
            raise RuntimeError("Camera not accessible")

    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return cv2.flip(frame, 1)

    def show(self, frame):
        cv2.imshow("Gesture Controller", frame)

    def is_opened(self):
        return self.cap.isOpened()

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
