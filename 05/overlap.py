#!/usr/bin/env python3

from collections import Counter
import math
import sys

class Canvas:
    """
    Represents a collection of 2D lines defined by their endpoints
    """

    def __init__(self, input_file):
        # Read the lines, one per line
        self._lines = [Line(l) for l in input_file]

    def __str__(self):
        # Reverse the read and format the lines
        output = [str(l) for l in self._lines]
        return "\n".join(output)

    def count_overlap(self, threshold, use_diagonals):
        """
        Core puzzle functionality: count the number of lines
        crossing points and count the number of points with
        a count above the specified threshold.
        """

        # Accumulate count using specialized dictionary by point
        grid = Counter()
        for line in self._lines:
            if line.is_cardinal() or use_diagonals:
                grid.update(line.get_points())

        # Count the number of counts above the threshold
        overlap = 0
        for count in grid.values():
            if count >= threshold:
                overlap += 1
        return overlap

class Line:
    """
    A 2D line segment with inclusive start and end points.
    """

    def __init__(self, input_string):
        # Read the line specification as two points
        (start, end) = input_string.strip().split(" -> ")
        self._start = Point(start)
        self._end = Point(end)

    def __str__(self):
        # Reverse the read and format the start and end points
        return "%s -> %s" % (self._start, self._end)

    def is_cardinal(self):
        """
        Check whether this line is strictly horizontal or vertical.
        """

        return self._start._x == self._end._x or self._start._y == self._end._y

    def get_points(self):
        """
        Generate all of the points in the line, including the endpoints.

        Only works in integer L1 norm space, supporting horizontal, vertical,
        and 45° diagonal lines.
        """

        # Determine the total horizontal and vertical distance between endpoints
        (x_range, y_range) = self._end.l1_range(self._start)

        # Determine which dimension determines the number of points
        max_range = max(abs(x_range), abs(y_range))

        # Determine the 2D step size between each point in the line
        (x_step, y_step) = (x_range/max_range, y_range/max_range)

        # Generate the points step by step, inclusive
        for step in range(max_range + 1):
            yield (self._start._x + step*x_step, self._start._y + step*y_step)

class Point:
    def __init__(self, input_string):
        # Read the comma-separated x,y point pair
        (self._x, self._y) = [int(n) for n in input_string.split(",")]

    def __str__(self):
        # Reverse the read and format the x and y values
        return "%d,%d" % (self._x, self._y)

    def l1_range(self, other):
        """
        Calculate a variant of the L1 norm, which is just the distance between
        this point and the specified other point along each axis.
        """

        return (self._x - other._x, self._y - other._y)

def main(input_path):
    """
    Entry point for puzzle day 2021.12.05
    """

    # Open the provided input
    with open(input_path) as input_file:
        # Initialize the map state from the input
        vents_map = Canvas(input_file)

        # Calculate and print results
        print("Cardinal Overlap: %d" % vents_map.count_overlap(2, False))
        print("Overlap: %d" % vents_map.count_overlap(2, True))

if __name__ == "__main__":
    main(sys.argv[1])
