#!/usr/bin/env python3

import re
import sys

"""
Process course commands to determine final position

When using aim, instead of up/down affecting depth
directly, they change the direction which in turn
changes the depth when moving forward.
"""
def navigate(course, use_aim = False):

    # Track current travel distance and depth and aim direction
    distance = 0
    depth = 0
    aim = 0
    for command in course:
        # Parse the command direction and value using a regular expression
        command_match = re.match(r"(\w+) (\d+)", command)
        direction = command_match.group(1)
        value = int(command_match.group(2))

        # Handle command direction and adjust behavior depending on whether aim flag is set
        if direction == "forward":
            distance += value
            if use_aim:
                depth += aim * value
        elif direction == "up":
            if use_aim:
                aim -= value
            else:
                depth -= value
        elif direction == "down":
            if use_aim:
                aim += value
            else:
                depth += value

    # Done, return final position as a distance-depth tuple
    return (distance, depth, distance*depth)

"""
Entry point for puzzle day 2021.12.02
"""
def main(input_path):
    # Open the provided input
    with open(input_path) as input_file:
        # Read the navigation course, one step per line
        course = [line.strip() for line in input_file]

        # Calculate and print results
        print("Final position: (%d, %d) = %d" % navigate(course))
        print("Final position with aiming: (%d, %d) = %d" % navigate(course, True))

if __name__ == "__main__":
    main(sys.argv[1])
