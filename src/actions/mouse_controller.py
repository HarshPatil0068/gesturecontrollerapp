import pyautogui
import time

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


class MouseController:
    def __init__(self):
        self.w, self.h = pyautogui.size()
        self.dragging = False
        self.last_click = 0

    def move(self, hand):
        tip = hand.landmark[8]

        tx = int((1 - tip.x) * self.w)
        ty = int(tip.y * self.h)

        if not hasattr(self, "px"):
            self.px, self.py = tx, ty

        # FAST smoothing (low latency)
        alpha = 0.6  # higher = faster

        x = int(self.px + (tx - self.px) * alpha)
        y = int(self.py + (ty - self.py) * alpha)

        pyautogui.moveTo(x, y, _pause=False)
        self.px, self.py = x, y



    def click(self):
        now = time.time()
        if now - self.last_click > 0.7:
            pyautogui.click()
            self.last_click = now

    def drag(self, hand):
        if not self.dragging:
            pyautogui.mouseDown()
            self.dragging = True
        self.move(hand)

    def release(self):
        if self.dragging:
            pyautogui.mouseUp()
            self.dragging = False

    def scroll(self, hand):
        #    DO NOT move cursor while scrolling
        dy = hand.landmark[8].y - hand.landmark[6].y

        # Dead zone
        if abs(dy) < 0.015:
         return

        amount = int(max(min(dy * 200, 80), -80))
        pyautogui.scroll(-amount)



    def swipe(self, direction):
        if direction == "LEFT":
            pyautogui.hotkey("alt", "left")
        elif direction == "RIGHT":
            pyautogui.hotkey("alt", "right")
