def classify_gesture(f):
    # Pause
    if f["thumb"] and f["index"] and not f["middle"]:
        return "PAUSE"

    # Fist → Drag
    if not any(f.values()):
        return "DRAG"

    # Scroll → 3 fingers
    if f["index"] and f["middle"] and f["ring"] and not f["pinky"]:
        return "SCROLL"

    # Click → Victory
    if f["index"] and f["middle"] and not f["ring"]:
        return "CLICK"

    # Move → Index only
    if f["index"] and not f["middle"] and not f["ring"]:
        return "MOVE"

    return "IDLE"
