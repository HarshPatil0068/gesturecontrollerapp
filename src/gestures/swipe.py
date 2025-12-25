from collections import deque

class SwipeDetector:
    def __init__(self, size=10, threshold=0.18):
        self.x = deque(maxlen=size)
        self.threshold = threshold

    def update(self, tip):
        self.x.append(tip.x)
        if len(self.x) < self.x.maxlen:
            return None

        dx = self.x[-1] - self.x[0]

        if dx > self.threshold:
            return "RIGHT"
        if dx < -self.threshold:
            return "LEFT"
        return None
