# --- Day 5: Binary Boarding ---

# You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport control.

# You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input); perhaps you can find your seat through process of elimination.

# Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".

# The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.

# For example, consider just the first seven characters of FBFBBFFRLR:

# Start by considering the whole range, rows 0 through 127.

# F means to take the lower half, keeping rows 0 through 63.
# B means to take the upper half, keeping rows 32 through 63.
# F means to take the lower half, keeping rows 32 through 47.
# B means to take the upper half, keeping rows 40 through 47.
# B keeps rows 44 through 47.
# F keeps rows 44 through 45.
# The final F keeps the lower of the two, row 44.

# The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.

# For example, consider just the last 3 characters of FBFBBFFRLR:

# Start by considering the whole range, columns 0 through 7.

# R means to take the upper half, keeping columns 4 through 7.
# L means to take the lower half, keeping columns 4 through 5.
# The final R keeps the upper of the two, column 5.

# So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

# Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.

# Here are some other boarding passes:

# BFFFBBFRRR: row 70, column 7, seat ID 567.
# FFFBBBFRRR: row 14, column 7, seat ID 119.
# BBFFBBFRLL: row 102, column 4, seat ID 820.

# As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?

# --- Part Two ---

# Ding! The "fasten seat belt" signs have turned on. Time to find your seat.

# It's a completely full flight, so your seat should be the only missing boarding pass in your list. However, there's a catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing from your list as well.

# Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.

# What is the ID of your seat?


from typing import List, Tuple

BoardingPass = Tuple[int,int]

def get_row_column(seat: str) -> BoardingPass:
    row_min = 0
    row_max = 128
    for x in seat[:8]:
        if x == 'F':
            row_max = (row_max + row_min) // 2
        else:
            row_min = (row_max + row_min) // 2
    row = row_min

    column_min = 0
    column_max = 8
    for y in seat[-3:]:
        if y == 'L':
            column_max = (column_min + column_max) // 2
        else:
            column_min = (column_min + column_max) // 2
    column = column_min

    return (row, column)

def parse_boarding_passes(_input: str) -> List[BoardingPass]:
    boarding_passes = list()
    with open(_input, 'r') as f:
        for line in f.readlines():
            boarding_passes.append(get_row_column(line.strip()))

    return boarding_passes

def get_seat_id(boarding_pass: BoardingPass) -> int:
    row, column = boarding_pass
    return row * 8 + column

def get_highest_seat_id(boarding_passes: List[BoardingPass]) -> int:
    highest_seat_id = 0

    for bp in boarding_passes:
        seat_id = get_seat_id(bp)
        highest_seat_id = max(highest_seat_id, seat_id)

    return highest_seat_id

def find_my_seat_id(boarding_passes: List[BoardingPass]) -> int:
    boarding_passes.sort(key=get_seat_id)

    for i in range(1, len(boarding_passes) - 1):
        curr = get_seat_id(boarding_passes[i])
        nxt = get_seat_id(boarding_passes[i+1])
        if nxt - curr != 1:
            return curr + 1

    return -1

def main() -> None:
    boarding_passes = parse_boarding_passes('input.txt')
    print('Part 1:', get_highest_seat_id(boarding_passes))
    print('Part 2:', find_my_seat_id(boarding_passes))

if __name__ == '__main__':
    main()
