import cProfile
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
        data: List = [[int(z) for z in y] for x in data for y in x]
    return data


def get_visibility_and_scenic_scores(numpy_grid, need_scenic=False):
    visible = 2 * numpy_grid.shape[0] + 2 * (numpy_grid.shape[0] - 2)
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
    return visible, highest_scenic_score, scenic_trees


def visibility_scenic_score_approach_2(file_data):
    row_length = len(file_data[0])
    edge = 2 * row_length + 2 * (row_length - 2)
    best_scenic_score = 0
    for ind, row in enumerate(file_data):
        if ind == 0 or ind == row_length - 1:
            continue
        for tree_ind, tree in enumerate(row):
            if tree_ind == 0 or tree_ind == row_length - 1:
                continue
            left = file_data[ind][0:tree_ind] if tree_ind > 1 else [file_data[ind][0]]
            right = file_data[ind][tree_ind + 1 :]
            up = (
                [x[tree_ind] for x in file_data[0:ind]]
                if ind > 1
                else [file_data[0][tree_ind]]
            )
            down = [x[tree_ind] for x in file_data[ind + 1 :]]
            up_visible = [tree > x for x in up]
            down_visible = [tree > x for x in down]
            left_visible = [tree > x for x in left]
            right_visible = [tree > x for x in right]

            left_ind = next((i + 1 for i, e in enumerate(left_visible) if not e), -1)
            right_ind = next((i + 1 for i, e in enumerate(right_visible) if not e), -1)
            up_ind = next((i + 1 for i, e in enumerate(up_visible) if not e), -1)
            down_ind = next((i + 1 for i, e in enumerate(down_visible) if not e), -1)

            visibility_scores = [left_ind, right_ind, up_ind, down_ind]
            if -1 in visibility_scores:
                left_ind_score = next(
                    (i + 1 for i, e in enumerate(left_visible) if not e),
                    len(left_visible),
                )
                right_ind_score = next(
                    (i + 1 for i, e in enumerate(right_visible) if not e),
                    len(right_visible),
                )
                up_ind_score = next(
                    (i + 1 for i, e in enumerate(up_visible) if not e), len(up_visible)
                )
                down_ind_score = next(
                    (i + 1 for i, e in enumerate(down_visible) if not e),
                    len(down_visible),
                )
                scenic_score = (
                    left_ind_score + right_ind_score + up_ind_score + down_ind_score
                )
                if scenic_score > best_scenic_score:
                    best_scenic_score = scenic_score
                edge += 1
    return edge, best_scenic_score


txt_file: str = "data/data_8.txt"
# txt_file: str = "./data/test.txt"
raw_data: List[List[int]] = list_read_buffer(txt_file)
# print(f"{file_data=}")

grid = np.array(raw_data)
# print(f"{grid.shape=}")

# print(grid)

print("Part 1")
print("--------------------------------------")

visible, scenic_highest_score, scenic_trees = get_visibility_and_scenic_scores(
    numpy_grid=grid
)

visible_trees, scenic_tree = visibility_scenic_score_approach_2(raw_data)


print(f"{visible_trees=}")

print()
print(f"{visible=}")


print()
print("Part 2")
print("--------------------------------------")
# print(f"{scenic_trees=}")
print(f"{scenic_highest_score=}")
print(f"{scenic_tree=}")


cProfile.run("get_visibility_and_scenic_scores(numpy_grid=grid)")
cProfile.run("visibility_scenic_score_approach_2(raw_data)")
