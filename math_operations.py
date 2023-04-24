import math

def ABS_ERROR(start, end):
    start_x, start_y = start[0] - 400, start[1] - 300
    end_x, end_y = end[0] - 400, end[1] - 300
    a = math.hypot(start_x, start_y)
    b = math.hypot(end_x, end_y)
    return abs(a - b)

def radi(start):
    x, y = start[0] - 400, start[1] - 300
    return math.hypot(x, y)