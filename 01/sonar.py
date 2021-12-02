#!/usr/bin/env python3

import sys

"""
Look for depth increases over arbitrarily large summed windows.
"""
def count_depth_increases(depths, window_size = 1):
    # Track increases and previous summed depth while looping through the depth readings
    increased = 0
    previous_depth = None
    for window_start in range(len(depths) - window_size + 1):
        # Sum the values over an array slice of the specified size
        depth = sum(depths[window_start:window_start+window_size])
        if previous_depth is not None and depth > previous_depth:
            # It's an increase if the curent summed depth window exceeds the previous one, if any
            increased += 1
        previous_depth = depth

    # Done, return total number of depth increases
    return increased

"""
Entry point for puzzle day 2021.12.01
"""
def main(input_path):
    # Open the provided input
    with open(input_path) as input_file:
        # Read all depths in one pass so we can reuse; one integer depth value per line
        depths = [int(line.strip()) for line in input_file]

        # Calculate and print results
        print("Depth increases: %d" % count_depth_increases(depths))
        print("Windowed depth increases: %d" % count_depth_increases(depths, 3))

if __name__ == "__main__":
    main(sys.argv[1])
