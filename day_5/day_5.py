import copy
from typing import List


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def list_read_buffer(file: str):
    with open(file, "rb") as f:
        c_generator = _count_generator(f.raw.read)
        data: List = [buffer.decode("utf-8").split("\n\n") for buffer in c_generator]
        data: List = [y.split("\n") for x in data for y in x]
    return data[0], data[1]


# txt_file: str = "data/data_5.txt"
txt_file: str = "./data/test.txt"
stacks, moves = list_read_buffer(txt_file)

number_of_stacks = max([int(x) for x in stacks[-1].strip().split(" ") if x != ""])
print(f"{number_of_stacks=}")

stack_start = [[] for i in range(number_of_stacks)]
for stack_line_number in range(len(stacks) - 2, -1, -1):
    stack_line = stacks[stack_line_number]
    stack_num = 0
    for i in range(0, number_of_stacks * 3 + number_of_stacks - 1, 4):
        container = stack_line[i : i + 3].strip()
        if container != "":
            stack_start[stack_num].insert(0, container)
        stack_num += 1
for item in stack_start:
    print(item)
# print(f"{stack_start=}")

print("Part 1")
print("--------------------------------------")

stack_start_1 = copy.deepcopy(stack_start)
for move in moves:
    order = move.split(" ")
    number_of_containers = int(order[1])
    starting_stack = int(order[3]) - 1
    ending_stack = int(order[5]) - 1
    # print(
    #     f"Move {number_of_containers} containers from {starting_stack} to {ending_stack}"
    # )

    # print(f"{starting_stack=}")
    # print(f"{ending_stack=}")

    # print(f"{[len(x) for x in stack_start]}")
    for i in range(number_of_containers):
        container = stack_start_1[starting_stack][0]
        del stack_start_1[starting_stack][0]
        # print(f"{container=}")

        # heappush(stack_start[ending_stack], container)
        stack_start_1[ending_stack].insert(0, container)

    # for item in stack_start:
    #     print(item)
    # print("-----------------------")
    # print()
    # print(f"{stack_start=}")
    # break
# print(f"{stack_start=}")

final_message = ""
for i in range(number_of_stacks):
    final_message += stack_start_1[i][0]
final_message = "".join([c for c in final_message if c not in ["[", "]"]])
print(f"{final_message=}")


print()
print("Part 2")
print("--------------------------------------")

stack_start_2 = copy.deepcopy(stack_start)
for move in moves:
    order = move.split(" ")
    number_of_containers = int(order[1])
    starting_stack = int(order[3]) - 1
    ending_stack = int(order[5]) - 1
    # print(
    #     f"Move {number_of_containers} containers from {starting_stack} to {ending_stack}"
    # )
    #
    # print(f"{starting_stack=}")
    # print(f"{ending_stack=}")

    # if number_of_containers == 1:
    #     container = stack_start_2[starting_stack][0:number_of_containers]
    #     print(f"{container=}")
    #     del stack_start_2[starting_stack][0:number_of_containers]
    #     for i in range(len(container) - 1, -1, -1):
    #         stack_start_2[ending_stack].insert(0, container[i])
    # else:

    containers = stack_start_2[starting_stack][0:number_of_containers]
    # print(f"{containers=}")
    del stack_start_2[starting_stack][0:number_of_containers]
    for i in range(len(containers) - 1, -1, -1):
        stack_start_2[ending_stack].insert(0, containers[i])

    # print(f"{[len(x) for x in stack_start]}")
    # for i in range(number_of_containers):
    #     container = stack_start_2[starting_stack][0]
    #     del stack_start_2[starting_stack][0]
    #     # print(f"{container=}")
    #
    #     # heappush(stack_start[ending_stack], container)
    #     stack_start_2[ending_stack].insert(0, container)

    # for item in stack_start_2:
    #     print(item)
    # print("-----------------------")
    # print()
    # print(f"{stack_start=}")
    # break
# print(f"{stack_start=}")

final_message = ""
for i in range(number_of_stacks):
    # print(stack_start_2[i][0])
    final_message += stack_start_2[i][0]
final_message = "".join([c for c in final_message if c not in ["[", "]"]])
print(f"{final_message=}")
