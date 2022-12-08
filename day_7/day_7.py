from typing import List, Dict
from anytree import Node, RenderTree
import json


def tree_example():
    udo = Node("Udo")
    marc = Node("Marc", parent=udo)
    lian = Node("Lian", parent=marc)
    dan = Node("Dan", parent=udo)
    jet = Node("Jet", parent=dan)
    jan = Node("Jan", parent=dan)
    joe = Node("Joe", parent=dan)

    print(udo)
    Node("/Udo")
    print(joe)
    Node("/Udo/Dan/Joe")

    for pre, fill, node in RenderTree(udo):
        print("%s%s" % (pre, node.name))

    # Udo
    # ├── Marc
    # │   └── Lian
    # └── Dan
    #     ├── Jet
    #     ├── Jan
    #     └── Joe

    print(dan.children)
    (Node("/Udo/Dan/Jet"), Node("/Udo/Dan/Jan"), Node("/Udo/Dan/Joe"))


def get_total_file_size(input, total: int, total_sizes: Dict):
    if isinstance(input, dict):
        tot = 0
        for key, val in input.items():
            if isinstance(val, dict):
                dict_total = get_total_file_size(val, tot, total_sizes)
                total_sizes[key] = dict_total
                tot += dict_total
            else:
                tot += val
        total += tot
    else:
        total += input
    return total


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def list_read_buffer(file: str):
    with open(file, "rb") as f:
        c_generator = _count_generator(f.raw.read)
        data: List = [buffer.decode("utf-8").split("$") for buffer in c_generator]
        data: List = [y.strip("\n").strip() for x in data for y in x if y != ""]
    return data


def solve(dir):
    if type(dir) == int:
        return (dir, 0)
    size = 0
    ans = 0
    for child in dir.values():
        s, a = solve(child)
        size += s
        ans += a
    if size <= 100000:
        ans += size
    return (size, ans)


txt_file: str = "data/data_7.txt"
# txt_file: str = "./data/test.txt"
file_data: List[str] = list_read_buffer(txt_file)
print(f"{file_data=}")

print("Part 1")
print("--------------------------------------")

# tree_example()

current_root = "/"
# root = Node(current_root)
file_struct: Dict = {}
cwd = []
for line in file_data:
    cmd = line.split("\n")

    command = cmd[0]
    if "cd" in command:
        dir = command.split()[1]
        if dir != "..":
            cwd.append(dir)
        else:
            del cwd[-1]
    else:
        items = cmd[1:]
        dirs = {x.replace("dir ", ""): {} for x in items if "dir" in x}

        files = {x.split()[1]: int(x.split()[0]) for x in items if "dir" not in x}

        tmp = file_struct
        for path in cwd[:-1]:
            tmp = tmp[path]

        tmp[cwd[-1]] = dict(dirs, **files)


# print(json.dumps(file_struct, sort_keys=True, indent=4))


total_root_size, total_less_than_100k = solve(file_struct)

print(f"{total_less_than_100k=}")

print()
print("Part 2")
print("--------------------------------------")


def size(dir):
    if type(dir) == int:
        return dir
    return sum(map(size, dir.values()))


t = total_root_size - 40_000_000
# print(f"{t=}")


def solve_smallest(dir):
    ans = float("inf")
    if size(dir) >= t:
        ans = size(dir)
    for child in dir.values():
        if type(child) == int:
            continue
        q = solve_smallest(child)
        ans = min(ans, q)
    return ans


smallest_dir_size = solve_smallest(file_struct)
print(f"{smallest_dir_size=}")
