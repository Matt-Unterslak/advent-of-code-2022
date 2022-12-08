from typing import List


def map_choice(chosen_play: str):
    match chosen_play:
        case "A":
            return 1
        case "B":
            return 2
        case "C":
            return 3
        case "X":
            return 1
        case "Y":
            return 2
        case "Z":
            return 3


def map_loss(opponent: str):
    # losing combinations:
    # Rock = 1, Paper = 2, Scissors = 3
    # (3,1),(2, 3),(1, 2)
    match opponent:
        case "A":
            return 3
        case "B":
            return 1
        case "C":
            return 2


def map_win(opponent: str):
    match opponent:
        case "A":
            return 2
        case "B":
            return 3
        case "C":
            return 1


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


txt_file: str = "./data/data_2.txt"
# txt_file: str = "./data/test.txt"
elf_data = list_read_buffer(txt_file)
print(f"{elf_data=}")

print("Part 1")
print("--------------------------------------")
numbers: List = [[map_choice(x[0]), map_choice(x[1])] for x in elf_data]
# winning combinations:
# Rock = 1, Paper = 2, Scissors = 3
# (3,1),(2, 3),(1, 2)
winning_combinations: List = [[3, 1], [2, 3], [1, 2]]

scores = []
for item in numbers:
    score = item[1]
    if item in winning_combinations:
        score += 6
    elif item[0] == item[1]:
        score += 3
    scores.append(score)

print(f"{scores=}")
total_score: int = sum(scores)
print(f"{total_score=}")

print("Part 2")
print("--------------------------------------")

new_scores: List[int] = []
plays: List = []
for item in elf_data:
    score = 0
    if item[1] == "X":
        choice = map_loss(item[0])
    elif item[1] == "Y":
        choice = map_choice(item[0])
        score += 3
    else:
        choice = map_win(item[0])
        score += 6

    score += choice
    plays.append([map_choice(item[0]), choice])
    new_scores.append(score)

print(f"{plays=}")
print(f"{new_scores=}")

total_score_new: int = sum(new_scores)
print(f"{total_score_new=}")
