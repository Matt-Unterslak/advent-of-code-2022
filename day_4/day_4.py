from typing import List, Dict


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def list_read_buffer(file: str):
    with open(file, "rb") as f:
        c_generator = _count_generator(f.raw.read)
        data: List = [buffer.decode("utf-8").split("\n") for buffer in c_generator]
        data: List = [y.split(",") for x in data for y in x]
    return data


txt_file: str = "data/data_4.txt"
# txt_file: str = "./data/test.txt"
file_data: List[str] = list_read_buffer(txt_file)
# print(f"{file_data=}")

print("Part 1")
print("--------------------------------------")

sections = []
overlapped_entirely = []
partially_overlap = []
for pair_1, pair_2 in file_data:
    start_1, end_1 = pair_1.split("-")
    start_2, end_2 = pair_2.split("-")

    set_1 = set([i for i in range(int(start_1), int(end_1) + 1)])
    set_2 = set([i for i in range(int(start_2), int(end_2) + 1)])

    if set_1.issubset(set_2) or set_2.issubset(set_1):
        overlapped = []
        overlapped.append(list(set_1))
        overlapped.append(list(set_2))
        overlapped_entirely.append(overlapped)

    if len(list(set_1.intersection(set_2))) > 0:
        partial_overlap = []
        partial_overlap.append(list(set_1))
        partial_overlap.append(list(set_2))
        partially_overlap.append(partial_overlap)

    total_set = []
    total_set.append(list(set_1))
    total_set.append(list(set_2))
    sections.append(total_set)

# print(f"{sections=}")
# print(f"{overlapped_entirely=}")
print(f"{len(overlapped_entirely)=}")

print()
print("Part 2")
print("--------------------------------------")

print(f"{len(partially_overlap)=}")
