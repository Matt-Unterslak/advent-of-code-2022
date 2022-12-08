import cProfile
from typing import List, Dict
import numpy as np
from functools import reduce


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def list_read_buffer(file: str):
    with open(file, "rb") as f:
        c_generator = _count_generator(f.raw.read)
        data: List = [buffer.decode("utf-8").split("\n") for buffer in c_generator]
        data: List = [[int(z) for z in y] for x in data for y in x]
    return data


def get_visibility_and_scenic_scores(numpy_grid, need_scenic=False):
    visible = 2 * numpy_grid.shape[0] + 2 * (numpy_grid.shape[0] - 2)
    # print(f"{visible=}")
    scenic_trees = []
    highest_scenic_score = 0
    for row in range(1, numpy_grid.shape[0] - 1):
        for col in range(1, numpy_grid.shape[1] - 1):
            grid_pos = [row, col]
            tree = numpy_grid[row, col]

            up_visible = down_visible = left_visible = right_visible = True
            scenic_scores = [0, 0, 0, 0]
            for i in range(1, numpy_grid.shape[0] - 1):
                # UP
                if up_visible is True:
                    up = (
                        numpy_grid[row - i, col] if row - i >= 0 else numpy_grid[0, col]
                    )
                    if tree <= up:
                        up_visible = False
                    if row - i >= 0:
                        scenic_scores[0] += 1

                # DOWN
                if down_visible is True:
                    down = (
                        numpy_grid[row + i, col]
                        if row + i <= numpy_grid.shape[0] - 1
                        else numpy_grid[numpy_grid.shape[0] - 1, col]
                    )
                    if tree <= down:
                        down_visible = False
                    if row + i <= numpy_grid.shape[0] - 1:
                        scenic_scores[1] += 1

                # LEFT
                if left_visible is True:
                    left = (
                        numpy_grid[row, col - i] if col - i >= 0 else numpy_grid[row, 0]
                    )
                    if tree <= left:
                        left_visible = False
                    if col - i >= 0:
                        scenic_scores[2] += 1

                # RIGHT
                if right_visible is True:
                    right = (
                        numpy_grid[row, col + i]
                        if col + i <= numpy_grid.shape[1] - 1
                        else numpy_grid[row, numpy_grid.shape[1] - 1]
                    )
                    if tree <= right:
                        right_visible = False
                    if col + i <= numpy_grid.shape[1] - 1:
                        scenic_scores[3] += 1
                if (
                    not up_visible
                    and not down_visible
                    and not left_visible
                    and not right_visible
                ):
                    break

            if up_visible or down_visible or left_visible or right_visible:
                total_scenic_score = (
                    scenic_scores[0]
                    * scenic_scores[1]
                    * scenic_scores[2]
                    * scenic_scores[3]
                )
                if total_scenic_score > highest_scenic_score:
                    highest_scenic_score = total_scenic_score
                if need_scenic:
                    scenic_trees.append([row, col, tree, total_scenic_score])
                visible += 1
            # print(row, col, tree, up_visible, down_visible, left_visible, right_visible)
    return visible, highest_scenic_score, scenic_trees


txt_file: str = "data/data_8.txt"
# txt_file: str = "./data/test.txt"
file_data: List[int] = list_read_buffer(txt_file)
# print(f"{file_data=}")

grid = np.array(file_data)
print(f"{grid.shape=}")

# print(grid)

print("Part 1")
print("--------------------------------------")

visible, highest_scenic_score, scenic_trees = get_visibility_and_scenic_scores(
    numpy_grid=grid
)

print()
print(f"{visible=}")


print()
print("Part 2")
print("--------------------------------------")
# print(f"{scenic_trees=}")
print(f"{highest_scenic_score=}")

cProfile.run("get_visibility_and_scenic_scores(numpy_grid=grid)")
