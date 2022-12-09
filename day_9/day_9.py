from typing import List

import numpy as np


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def list_read_buffer(file: str):
    with open(file, "rb") as f:
        c_generator = _count_generator(f.raw.read)
        data: List = [buffer.decode("utf-8").split("\n") for buffer in c_generator]
        data: List = [[y.split()[0], int(y.split()[1])] for x in data for y in x]
    return data


def add_tuples(tuple_1, tuple_2):
    return tuple(np.add(tuple_1, tuple_2))


def subtract_tuples(tuple_1, tuple_2):
    return tuple(np.subtract(tuple_1, tuple_2))


def new_position(head, tail):
    head_tail_diff = subtract_tuples(head, tail)
    difference = tuple(min(1, max(-1, x)) for x in head_tail_diff)
    if head_tail_diff != difference:
        return add_tuples(tail, difference)
    return tail


txt_file: str = "data/data_9.txt"
# txt_file: str = "./data/test.txt"
# txt_file: str = "./data/test_2.txt"
file_data: List[str] = list_read_buffer(txt_file)
print(f"{file_data=}")


DIRECTIONS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}

print("Part 1")
print("--------------------------------------")

head_pos = tail_pos = (0, 0)
tail_positions = set()
tail_positions.add(tail_pos)


for direction, steps in file_data:
    for i in range(steps):
        head_pos = add_tuples(head_pos, DIRECTIONS[direction])

        tail_pos = new_position(head_pos, tail_pos)
        tail_positions.add(tail_pos)

print(f"{len(tail_positions)=}")

print()
print("Part 2")
print("--------------------------------------")

rope = [(0, 0) for i in range(10)]

tail_positions = set()
tail_positions.add(rope[0])  # all positions are equivalent

for direction, steps in file_data:
    for i in range(steps):
        rope[0] = add_tuples(rope[0], DIRECTIONS[direction])

        for j in range(len(rope) - 1):
            rope[j + 1] = new_position(rope[j], rope[j + 1])
        tail_positions.add(rope[9])

print(f"{len(tail_positions)=}")
