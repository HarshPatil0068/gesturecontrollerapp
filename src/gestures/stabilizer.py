from collections import deque

class GestureStabilizer:
    def __init__(self, size=5, threshold=3):
        self.buf = deque(maxlen=size)
        self.threshold = threshold

    def update(self, g):
        self.buf.append(g)
        if self.buf.count(g) >= self.threshold:
            return g
        return None
