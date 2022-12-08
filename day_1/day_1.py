from typing import List


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def list_read_buffer(file: str):
    with open(file, "rb") as f:
        c_generator = _count_generator(f.raw.read)
        data = [buffer.decode("utf-8").split("\n\n") for buffer in c_generator]
        data = [[int(z) for z in y.split("\n")] for x in data for y in x]
    return data


txt_file: str = "./data/data_1.txt"
elf_data: List[List[int]] = list_read_buffer(txt_file)

print("Part 1")
print("-------------------------------")

elf_total_calories: List[int] = [sum(x) for x in elf_data]

max_elf_calories: int = max(elf_total_calories)
print(f"Max Elf Calories: {max_elf_calories}")

print()
print("Part 2")
print("-------------------------------")
sorted_calories: List[int] = sorted(elf_total_calories, reverse=True)
top_three: List[int] = sorted_calories[:3]
print(f"Top three elves: {top_three}")
sum_top_three: int = sum(top_three)
print(f"Sum Top Three Elf Calories: {sum_top_three}")
