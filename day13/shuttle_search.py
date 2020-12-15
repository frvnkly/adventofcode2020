# --- Day 13: Shuttle Search ---

# Your ferry can make it safely to a nearby port, but it won't get much further. When you call to book another ship, you discover that no ships embark from that port to your vacation island. You'll need to get from the port to the nearest airport.

# Fortunately, a shuttle bus service is available to bring you from the sea port to the airport! Each bus has an ID number that also indicates how often the bus leaves for the airport.

# Bus schedules are defined based on a timestamp that measures the number of minutes since some fixed reference point in the past. At timestamp 0, every bus simultaneously departed from the sea port. After that, each bus travels to the airport, then various other locations, and finally returns to the sea port to repeat its journey forever.

# The time this loop takes a particular bus is also its ID number: the bus with ID 5 departs from the sea port at timestamps 0, 5, 10, 15, and so on. The bus with ID 11 departs at 0, 11, 22, 33, and so on. If you are there when the bus departs, you can ride that bus to the airport!

# Your notes (your puzzle input) consist of two lines. The first line is your estimate of the earliest timestamp you could depart on a bus. The second line lists the bus IDs that are in service according to the shuttle company; entries that show x must be out of service, so you decide to ignore them.

# To save time once you arrive, your goal is to figure out the earliest bus you can take to the airport. (There will be exactly one such bus.)

# For example, suppose you have the following notes:

# 939
# 7,13,x,x,59,x,31,19

# Here, the earliest timestamp you could depart is 939, and the bus IDs in service are 7, 13, 59, 31, and 19. Near timestamp 939, these bus IDs depart at the times marked D:

# time   bus 7   bus 13  bus 59  bus 31  bus 19
# 929      .       .       .       .       .
# 930      .       .       .       D       .
# 931      D       .       .       .       D
# 932      .       .       .       .       .
# 933      .       .       .       .       .
# 934      .       .       .       .       .
# 935      .       .       .       .       .
# 936      .       D       .       .       .
# 937      .       .       .       .       .
# 938      D       .       .       .       .
# 939      .       .       .       .       .
# 940      .       .       .       .       .
# 941      .       .       .       .       .
# 942      .       .       .       .       .
# 943      .       .       .       .       .
# 944      .       .       D       .       .
# 945      D       .       .       .       .
# 946      .       .       .       .       .
# 947      .       .       .       .       .
# 948      .       .       .       .       .
# 949      .       D       .       .       .

# The earliest bus you could take is bus ID 59. It doesn't depart until timestamp 944, so you would need to wait 944 - 939 = 5 minutes before it departs. Multiplying the bus ID by the number of minutes you'd need to wait gives 295.

# What is the ID of the earliest bus you can take to the airport multiplied by the number of minutes you'll need to wait for that bus?


from typing import Tuple, List
import math

def parse_notes(_input: str) -> Tuple[int, List[str]]:
    with open(_input, 'r') as f:
        timestamp = int(f.readline().strip())
        bus_ids = f.readline().strip().split(',')
        return timestamp, bus_ids

def find_earliest_bus(timestamp: int, bus_ids: List[str]) -> Tuple[int, int]:
    earliest_bus = None
    least_wait = math.inf

    for b in bus_ids:
        if b == 'x':
            continue
        else:
            trip_length = int(b)
            wait = (math.ceil(timestamp / trip_length) * trip_length) - timestamp

            if wait < least_wait:
                earliest_bus = trip_length
                least_wait = wait

    return earliest_bus, least_wait

def modular_inverse(k: int, mod: int) -> int:
    for n in range(mod - 1):
        if (k * n) % mod == 1:
            print(k, mod, n)
            return n

def find_special_timestamp(bus_ids: List[str]) -> int:
    buses = list()
    id_prod = 1

    for i in range(len(bus_ids)):
        if bus_ids[i] == 'x':
            pass
        else:
            _id = int(bus_ids[i])
            buses.append((_id, i))
            id_prod *= _id
    
    special_timestamp = 0
    print(id_prod)
    for b in buses:
        k = id_prod // b[0]
        special_timestamp += b[1] * k * modular_inverse(k, b[0])

    return special_timestamp % id_prod

def main() -> None:
    timestamp, bus_ids = parse_notes('input.txt')
    
    earliest_bus, least_wait = find_earliest_bus(timestamp, bus_ids)
    print('Part 1:', earliest_bus * least_wait)

    # print('Part 2:', find_special_timestamp(bus_ids))

    return

if __name__ == '__main__':
    main()
