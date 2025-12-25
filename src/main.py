import time
import cv2

from camera.webcam import Webcam
from tracking.hand_tracker import HandTracker
from gestures.finger_state import get_finger_states
from gestures.classifier import classify_gesture
from gestures.stabilizer import GestureStabilizer
from gestures.swipe import SwipeDetector
from actions.mouse_controller import MouseController


def main():
    cam = Webcam()
    tracker = HandTracker()
    stabilizer = GestureStabilizer()
    swipe = SwipeDetector()
    mouse = MouseController()

    paused = False
    pause_time = 0

    frame_count = 0
    drag_start = 0

    while cam.is_opened():
        frame = cam.read()
        if frame is None:
            break

        frame_count += 1

        # --- PROCESS EVERY FRAME (IMPORTANT) ---
        hand = tracker.process(frame)

        if hand:
            fingers = get_finger_states(hand)
            gesture = classify_gesture(fingers)
            stable = stabilizer.update(gesture)

            # ---- PAUSE TOGGLE ----
            if stable == "PAUSE":
                if time.time() - pause_time > 1:
                    paused = not paused
                    pause_time = time.time()

            if not paused:
                if stable == "MOVE":
                    drag_start = 0
                    mouse.move(hand)

                    s = swipe.update(hand.landmark[8])
                    if s:
                        mouse.swipe(s)

                elif stable == "CLICK":
                    drag_start = 0
                    mouse.click()

                elif stable == "DRAG":
                    if drag_start == 0:
                        drag_start = time.time()
                    elif time.time() - drag_start > 0.4:
                        mouse.drag(hand)

                elif stable == "SCROLL":
                    drag_start = 0
                    mouse.scroll(hand)

                else:
                    drag_start = 0
                    mouse.release()
            else:
                drag_start = 0
                mouse.release()

            # --- DEBUG TEXT ---
            cv2.putText(frame, f"Gesture: {stable}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, f"Paused: {paused}", (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        # --- FPS OPTIMIZATION: DRAW EVERY 2nd FRAME ---
        if frame_count % 2 == 0:
            cam.show(frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam.release()


if __name__ == "__main__":
    main()
