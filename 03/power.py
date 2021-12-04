#!/usr/bin/env python3

import sys

"""
Shared helper method that counts the number of high
bits in each place across all input records
"""
def count_high_bits(records):
    # Track how many times we see a high bit in each place
    high_bit_counts = []
    for record in records:
        # Loop until we've shifted the binary value all the way to 0
        index = 0
        value = record
        while value > 0:
            # Don't know length of each input so make sure we have enough places
            if len(high_bit_counts) <= index:
                high_bit_counts.append(0)

            # Bitwise and extracts least significant bit
            bit = value & 1

            # If it's 1, add it in, so we're counting the 1s in each place
            high_bit_counts[index] += bit

            # Shift the bits left and increment our index
            value >>= 1
            index += 1

    return high_bit_counts


"""
Process records for energy usage

We're deriving gamma and epsilon values based on
which places were mostly high bits or mostly low bits.
"""
def calculate_energy_usage(records):
    # Determine high bit counts by place in input
    high_bit_counts = count_high_bits(records)

    # Determine gamma and epsilon bits
    #   Not doing this bitwise so we get padding as needed
    gamma_bits = []
    epsilon_bits = []
    for high_bit_count in high_bit_counts:
        # Gamma bit is high if high bit was in the majority in that place in the input records
        if high_bit_count > len(records) - high_bit_count:
            gamma_bits.append("1")
            epsilon_bits.append("0")
        else:
            gamma_bits.append("0")
            epsilon_bits.append("1")

    # Flip the bit order and convert strings to binary integer value
    gamma = int("".join(reversed(gamma_bits)), 2)
    epsilon = int("".join(reversed(epsilon_bits)), 2)

    # Done, return final energy usage
    return (gamma, epsilon, gamma*epsilon)

"""
Shared helper that reduces a set of records to a single record
by repeatedly looking for remaining records that have the
majority or minority bit in a particular place.
"""
def get_rating(records, use_majority):
    # Copy the input and initialize our bitwise counts, tracking place mask
    ratings = records
    high_bit_counts = count_high_bits(ratings)
    mask = 2**(len(high_bit_counts)-1)

    # Loop until a single record remains
    while len(ratings) > 1:
        # Use bitwise and to split the current records into two sets
        high_bit_ratings = [r for r in ratings if (r & mask) == mask]
        low_bit_ratings = [r for r in ratings if (r & mask) == 0]

        # Check which bit (high or low) is in the majority for this place
        if len(high_bit_ratings) >= len(low_bit_ratings):
            if use_majority:
                ratings = high_bit_ratings
            else:
                ratings = low_bit_ratings
        else:
            if use_majority:
                ratings = low_bit_ratings
            else:
                ratings = high_bit_ratings

        # Update the bit counts for the reduced records and shift the mask one place
        high_bit_counts = count_high_bits(ratings)
        mask >>= 1

    # Done, return the single remaining record
    return ratings[0]

"""
Process records for life support

The same approach is used for oxygeon and CO2, we just
reverse whether we're looking for the majority or minority
bits in each place in the remaining records.
"""
def calculate_life_rating(records):
    # Find oxygen generator and CO2 scrubber ratings
    oxygen = get_rating(records, use_majority=True)
    co2 = get_rating(records, use_majority=False)

    # Done, return final life support rating
    return (oxygen, co2, oxygen*co2)

"""
Entry point for puzzle day 2021.12.03
"""
def main(input_path):
    # Open the provided input
    with open(input_path) as input_file:
        # Read the log records, one binary value as a string per line
        records = [int(line.strip(), 2) for line in input_file]

        # Calculate and print results
        print("Energy usage: (%d, %d) = %d" % calculate_energy_usage(records))
        print("Life support rating: (%d, %d) = %d" % calculate_life_rating(records))

if __name__ == "__main__":
    main(sys.argv[1])
