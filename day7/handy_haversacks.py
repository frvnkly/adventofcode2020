# --- Day 7: Handy Haversacks ---

# You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

# Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

# For example, consider the following rules:

# light red bags contain 1 bright white bag, 2 muted yellow bags.
# dark orange bags contain 3 bright white bags, 4 muted yellow bags.
# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.

# These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

# You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

# In the above rules, the following options would be available to you:

# A bright white bag, which can hold your shiny gold bag directly.
# A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
# A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
# A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.

# So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

# How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)

# --- Part Two ---

# It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

# Consider again your shiny gold bag and the rules from the above example:

# faded blue bags contain 0 other bags.
# dotted black bags contain 0 other bags.
# vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
# dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.

# So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

# Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

# Here's another example:

# shiny gold bags contain 2 dark red bags.
# dark red bags contain 2 dark orange bags.
# dark orange bags contain 2 dark yellow bags.
# dark yellow bags contain 2 dark green bags.
# dark green bags contain 2 dark blue bags.
# dark blue bags contain 2 dark violet bags.
# dark violet bags contain no other bags.

# In this example, a single shiny gold bag must contain 126 other bags.

# How many individual bags are required inside your single shiny gold bag?


from typing import Dict, List, Tuple

BagGraph = Dict[str, List[Tuple[int, str]]]

def build_bag_graph(_input: str) -> BagGraph:
    bags = dict()
    with open(_input, 'r') as f:
        for line in f.readlines():
            bag, contents = line.strip().split(' contain ')

            bag_color = ' '.join(bag.split(' ')[:-1])
            bags[bag_color] = list()

            for content in contents.split(', '):
                spec = content.split(' ')

                if spec[0] == 'no':
                    continue
                else:
                    num = int(spec[0])
                    color = ' '.join(spec[1:-1])
                    bags[bag_color].append((num, color))

    return bags

def count_possible_containers(bags: BagGraph, target: str) -> int:
    num_possible_containers = 0

    memo = set()
    memo.add(target)

    for start in bags.keys():
        stack = [[start]]
        while len(stack):
            path = stack.pop()            

            if path[-1] in memo:
                for n in path:
                    if not n in memo:
                        num_possible_containers += 1
                        memo.add(n)
                continue
            
            for b in bags[path[-1]]:
                stack.append(path + [b[1]])

    return num_possible_containers

def sum_contents(bags: BagGraph, bag: str) -> int:
    def helper(bag: str, n: int) -> str:
        subtotal = 1
        
        for b in bags[bag]:
            subtotal += helper(b[1], b[0])

        return subtotal * n

    total = 0
    for b in bags[bag]:
        total += helper(b[1], b[0])
    return total

def main() -> None:
    bags = build_bag_graph('input.txt')
    print('Part 1:', count_possible_containers(bags, 'shiny gold'))
    print('Part 2:', sum_contents(bags, 'shiny gold'))

if __name__ == '__main__':
    main()
