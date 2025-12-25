def get_finger_states(hand):
    lm = hand.landmark
    return {
        "thumb":  lm[4].x > lm[3].x,
        "index":  lm[8].y < lm[6].y,
        "middle": lm[12].y < lm[10].y,
        "ring":   lm[16].y < lm[14].y,
        "pinky":  lm[20].y < lm[18].y,
    }
