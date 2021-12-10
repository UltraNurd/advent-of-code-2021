#!/usr/bin/env python3

import sys

def read_signals(input_file):
    """
    Load all of the signal input and output readings into a list
    of dictionaries.
    """

    signals = []
    for line in input_file:
        (signal, digits) = line.strip().split(" | ")
        signals.append({"signal":signal.split(" "), "output":digits.split(" ")})
    return signals

def get_unique_output_values(signals):
    """
    Based on segment length, determine how many of the possible four
    uniquely identifiable digits are in the set of signals.
    """

    unique_digit_count = 0
    for signal in signals:
        for digit in signal["output"]:
            if len(digit) in (2, 3, 4, 7):
                unique_digit_count += 1
    return unique_digit_count

# Standard mapping of sorted segment IDs to digit values
actual_digit_segments = {
    "abcefg":"0",
    "cf":"1",
    "acdeg":"2",
    "acdfg":"3",
    "bcdf":"4",
    "abdfg":"5",
    "abdefg":"6",
    "acf":"7",
    "abcdefg":"8",
    "abcdfg":"9"
}

def get_decoded_values(signals):
    """
    Use deduction from uniquely identifiable digits to identify
    the segment decoding necessary to convert each signal output
    into its true value.
    """

    values = []
    for signal in signals:
        # Normalize the unique digits in the signal
        digits = set(["".join(set(digit)) for digit in signal["signal"] + signal["output"]])

        # Track mapping from known 0-9 values to their segment sets
        digit_segments = {}

        # Track segment mapping from signal to actual
        signal_decoder = {}

        # We know the four digits with a unique size
        for digit in digits:
            if len(digit) == 2:
                value = 1
            elif len(digit) == 3:
                value = 7
            elif len(digit) == 4:
                value = 4
            elif len(digit) == 7:
                value = 8
            else:
                value = None
            if value is not None:
                digit_segments[value] = digit
        for digit in digit_segments.values():
            digits.remove(digit)

        # We know the top segment from difference between 7 and 1
        signal_decoder[min(set(digit_segments[7]) - set(digit_segments[1]))] = "a"

        # Find 9 by masking 4 and 7 from it, then mask it from 8
        for digit in digits:
            if len(digit) == 6:
                maybe_nine = set(digit) - set(digit_segments[4]) - set(digit_segments[7])
                if len(maybe_nine) == 1:
                    digit_segments[9] = digit
                    signal_decoder[min(maybe_nine)] = "g"
                    signal_decoder[min(set(digit_segments[8]) - set(digit_segments[9]))] = "e"
        digits.remove(digit_segments[9])

        # Find 0 and 6 by masking from 8 and checking against 1
        for digit in digits:
            if len(digit) == 6:
                d_or_c = min(set(digit_segments[8]) - set(digit))
                one = set(digit_segments[1])
                if d_or_c in one:
                    digit_segments[6] = digit
                    signal_decoder[d_or_c] = "c"
                    signal_decoder[min(one - set(d_or_c))] = "f"
                else:
                    digit_segments[0] = digit
                    signal_decoder[d_or_c] = "d"
        digits.remove(digit_segments[0])
        digits.remove(digit_segments[6])

        # Find 3 by masking from 8 and checking against 1
        for digit in digits:
            if len(digit) == 5:
                pair = set(digit_segments[8]) - set(digit)
                one_remainder = pair - set(digit_segments[1])
                if len(one_remainder) == 2:
                    digit_segments[3] = digit
                    for maybe_b in one_remainder:
                        if maybe_b not in signal_decoder:
                            signal_decoder[maybe_b] = "b"
                    break

        # We have all the segments, don't need to actually distinguish between 2 and 5

        # Finally decode the output, mapping segments to digits and converting the string to the final integer value
        value_digits = []
        for encoded in signal["output"]:
            decoded = "".join(sorted([signal_decoder[c] for c in encoded]))
            digit = actual_digit_segments[decoded]
            value_digits.append(digit)
        value = int("".join(value_digits))
        values.append(value)

    # Done
    return values

def main(input_path):
    """
    Entry point for puzzle day 2021.12.08
    """

    # Open the provided input
    with open(input_path) as input_file:
        # Read the digit signal input
        signals = read_signals(input_file)

        # Calculate and print results
        print("Unique output values: %d" % get_unique_output_values(signals))
        print("Decoded sum: %d" % sum(get_decoded_values(signals)))

if __name__ == "__main__":
    main(sys.argv[1])
