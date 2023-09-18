class GameMath:
    def __init__(self):
        pass

    def is_counter_clockwise(self, pointA, pointB, pointC):
        return (pointC[1] - pointA[1]) * (pointB[0] - pointA[0]) > (pointB[1] - pointA[1]) * (pointC[0] - pointA[0])

    def do_lines_intersect(self, line1_start, line1_end, line2_start, line2_end):
        return (self.is_counter_clockwise(line1_start, line2_start, line2_end) !=
                self.is_counter_clockwise(line1_end, line2_start, line2_end)) and \
            (self.is_counter_clockwise(line1_start, line1_end, line2_start) !=
             self.is_counter_clockwise(line1_start, line1_end, line2_end))
