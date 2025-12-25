def smooth(prev, curr, alpha):
    return int(prev + (curr - prev) * alpha)
