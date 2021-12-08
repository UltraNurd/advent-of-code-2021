#!/usr/bin/env python3

from collections import Counter
import sys

class School:
    """
    Represents a population of fish.
    """

    def __init__(self, input_file):
        # Read the single line of initial timers
        self._fish = Counter([int(i) for line in input_file for i in line.strip().split(",")])

    def __str__(self):
        # Dump the count dictionary
        return str(sorted(self._fish.items()))

    def reproduce(self, days):
        for day in range(days):
            next_fish = Counter()
            for fish, count in self._fish.items():
                if fish == 0:
                    next_fish.update({6:count, 8:count})
                else:
                    next_fish.update({fish-1:count})
            self._fish = next_fish

    def get_size(self):
        return sum(self._fish.values())

def main(days, input_path):
    """
    Entry point for puzzle day 2021.12.06
    """

    # Open the provided input
    with open(input_path) as input_file:
        # Initialize the fish state from the input
        school = School(input_file)

        # Calculate and print results
        school.reproduce(int(days))
        print("Lanternfish population: %d" % school.get_size())

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
