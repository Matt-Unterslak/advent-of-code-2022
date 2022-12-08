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
        data: List = [y for x in data for y in x]
    return data


txt_file: str = "data/data_6.txt"
# txt_file: str = "./data/test.txt"
file_data: List[str] = list_read_buffer(txt_file)
print(f"{file_data=}")

print("Part 1")
print("--------------------------------------")

first_marker_locations = []
for msg in file_data:
    first = msg[:4]
    if len(set(first)) == 4:
        first_marker_locations.append(3)
        continue
    else:
        for i in range(4, len(msg)):
            first = msg[i - 3 : i + 1]
            if len(set(first)) == 4:
                first_marker_locations.append(i + 1)
                break

print(f"{first_marker_locations=}")
print()
print("Part 2")
print("--------------------------------------")

start_of_message_markers = []
for msg in file_data:
    first = msg[:14]
    if len(set(first)) == 14:
        start_of_message_markers.append(14)
        continue
    else:
        for i in range(14, len(msg)):
            first = msg[i - 13 : i + 1]
            if len(set(first)) == 14:
                start_of_message_markers.append(i + 1)
                break

print(f"{start_of_message_markers=}")
