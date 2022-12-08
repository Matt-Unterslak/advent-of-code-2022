from typing import List, Dict

import string


def char_values():
    values = dict()
    letters = string.ascii_lowercase + string.ascii_uppercase
    for index, letter in enumerate(letters):
        values[letter] = index + 1
    return values


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def list_read_buffer(file: str):
    with open(file, "rb") as f:
        c_generator = _count_generator(f.raw.read)
        data: List = [buffer.decode("utf-8").split("\n") for buffer in c_generator]
        data: List = [y for x in data for y in x]
    return data


txt_file: str = "data/data_3.txt"
# txt_file: str = "./data/test.txt"
rucksack_data: List[str] = list_read_buffer(txt_file)
rucksack_items: List = [
    [x, x[: len(x) // 2], x[(len(x) // 2) :]] for x in rucksack_data
]
print(f"{rucksack_items=}")

print("Part 1")
print("--------------------------------------")

common_items = ["".join(set(x[1]).intersection(x[2])) for x in rucksack_items]
print(f"{common_items=}")

chars: Dict[str, int] = char_values()
print(f"{chars=}")

# item_values = [[x, chars[x]] for x in common_items]
item_values = [chars[x] for x in common_items]
print(f"{item_values=}")

sum_of_items: int = sum(item_values)
print(f"{sum_of_items=}")


print()
print("Part 2")
print("--------------------------------------")
rucksack_groups: List = []
tmp = []
for i, v in enumerate(rucksack_data):
    # print(i, i % 3, tmp)
    if i == 0:
        tmp.append(v)
    elif i % 3 == 0:
        # print(tmp)
        rucksack_groups.append(tmp)
        tmp = [v]
    else:
        tmp.append(v)
rucksack_groups.append(tmp)
print(f"{rucksack_data=}")
print(f"{rucksack_groups=}")

common_group_items: List = []
for a, b, c in rucksack_groups:
    common = list(set(a) & set(b) & set(c))
    if len(common) == 1:
        common_group_items.append(common[0])
    else:
        carried = {c: sum([a.count(c), b.count(c), c.count(c)]) for c in common}
        max_count = max([v for _, v in carried.items()])
        final_common = [k for k, v in carried.items() if v == max_count]
        common_group_items.append(final_common[0])

# print(f"{common_group_items=}")

common_item_values = [chars[x] for x in common_group_items]
print(f"{common_item_values=}")

sum_of_item_values: int = sum(common_item_values)
print(f"{sum_of_item_values=}")
