#!/usr/bin/env python3

import math
import sys

class Swarm:
    """
    Represents a fleet of crab submarines and finds efficient movements for them.
    """

    def __init__(self, input_file):
        # Read the single line of initial positions
        self._crabs = [int(i) for line in input_file for i in line.strip().split(",")]

    def __str__(self):
        # Reverse the read and print the positions
        return ",".join([str(crab) for crab in self._crabs])

    def calculate_linear_move(self):
        """
        Given linear fuel cost (one movement uses one fuel unit),
        determine optimal final position and total fuel usage.

        In all cases this will be the median of the starting positions of all crabs.
        """

        median_position = self.calculate_median()
        fuel_expense = sum([abs(crab - median_position) for crab in self._crabs])
        return (median_position, fuel_expense)

    def calculate_median(self):
        """
        Find the median of crab position values
        """

        # Sort the crabs by position and get the midpoint
        sorted_crabs = sorted(self._crabs)
        midpoint = (len(sorted_crabs) - 1) // 2

        # Check even or odd cardinality
        if midpoint % 2:
            # Odd, take middle crab's position
            return sorted_crabs[midpoint]
        else:
            # Even, take average of two middle crabs' positions
            return (sorted_crabs[midpoint] + sorted_crabs[midpoint + 1]) / 2

    def calculate_arithmetic_move(self):
        """
        Given arithmetic fuel cost (each movement uses one more fuel unit),
        determine optimal final position and total fuel usage.

        Starts from the median position (which whould be close to optimal)
        and then performs gradient descent until we find the lowest fuel usage.
        """

        # Start from the median position
        optimal_position = self.calculate_median()
        optimal_fuel = self.calculate_triangular_distance(optimal_position)

        # Loop until we're at a local minimum (which should be an absolute minimum)
        while True:
            # Check left and right
            left_position = optimal_position - 1
            right_position = optimal_position + 1

            # The arithmetic fuel usage can be calculated with triangular numbers
            left_fuel = self.calculate_triangular_distance(left_position)
            right_fuel = self.calculate_triangular_distance(right_position)

            # Check if we should move left or right or are done
            if optimal_fuel is None or left_fuel < optimal_fuel:
                optimal_fuel = left_fuel
                optimal_position = left_position
            elif right_fuel < optimal_fuel:
                optimal_fuel = right_fuel
                optimal_position = right_position
            else:
                return (optimal_position, optimal_fuel)

    def calculate_triangular_distance(self, position):
        """
        The total fuel consumption given a position can be calculated quickly
        for its arithmetic series behavior using the triangular number formula
        n(n+1)/2
        """

        fuel = 0
        for crab in self._crabs:
            distance = abs(crab - position)
            fuel += distance*(distance + 1)/2
        return fuel

def main(input_path):
    """
    Entry point for puzzle day 2021.12.07
    """

    # Open the provided input
    with open(input_path) as input_file:
        # Initialize the crab state from the input
        swarm = Swarm(input_file)

        # Calculate and print results
        print("Optimal linear move: %d (%d fuel)" % swarm.calculate_linear_move())
        print("Optimal arithmetic move: %d (%d fuel)" % swarm.calculate_arithmetic_move())

if __name__ == "__main__":
    main(sys.argv[1])
