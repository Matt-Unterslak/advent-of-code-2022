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
        data: List = [y.split() for x in data for y in x]
    return data


# txt_file: str = "data/data_10.txt"
# txt_file: str = "./data/test.txt"
txt_file: str = "./data/test_2.txt"
file_data: List[str] = list_read_buffer(txt_file)
print(f"{file_data=}")

X = 1
cycles = []
print("Part 1")
print("--------------------------------------")
for instruction in file_data:
    if len(instruction) == 1:
        cycles.append(X)
    else:
        cycles.append(X)
        cycles.append(X)
        X += int(instruction[1])

cycles_wanted = [20, 60, 100, 140, 180, 220]
x_values = [[cycles[x - 1], cycles[x - 1] * x] for x in cycles_wanted]
total_sum = sum([x[1] for x in x_values])
print(f"{x_values=}")
print(f"{total_sum=}")


print()
print("Part 2")
print("--------------------------------------")

X = 1
clock = 0


def screen_printer(clock_time, register_value):
    # the value of the clock_time gives both the row and the position within that row.
    # the mod is used because the register is just a position
    if clock_time % 40 in (register_value - 1, register_value, register_value + 1):
        print("#", end="")
    else:
        print(".", end="")
    clock_time += 1
    if clock_time % 40 == 0:
        print()
    return clock_time


for instruction in file_data:
    if len(instruction) == 1:
        clock = screen_printer(clock, X)
    else:
        clock = screen_printer(clock, X)
        clock = screen_printer(clock, X)
        X += int(instruction[1])
