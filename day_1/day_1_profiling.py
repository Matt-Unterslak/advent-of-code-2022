import cProfile
from itertools import groupby
from ast import literal_eval as le
from typing import List

from utils.data import read_text_file_to_list

import numpy as np

TXT_FILE: str = "./data/data_1.txt"


def numpy_read():
    array_list = []
    with open(TXT_FILE) as f_data:
        for k, g in groupby(f_data, lambda x: x.startswith("\n")):
            if not k:
                array_list.append(
                    np.array(
                        [[float(x) for x in d.split()] for d in g if len(d.strip())]
                    )
                )
    return array_list


def list_read_util():
    data: List[str] = read_text_file_to_list(TXT_FILE)

    # print("Part 1")
    # print("-------------------------------")
    elf: List[int] = []
    elf_data: List[List[int]] = []
    for item in data:
        if item != "\n":
            elf.append(int(item.strip("\n")))
        else:
            elf_data.append(elf)
            elf = []
    return elf_data


def list_read():
    with open(TXT_FILE, "r") as f:
        # print("Part 1")
        # print("-------------------------------")
        elf: List[int] = []
        elf_data: List[List[int]] = []
        for item in f:
            if item != "\n":
                elf.append(int(item.strip("\n")))
            else:
                elf_data.append(elf)
                elf = []
        return elf_data


def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)


def list_read_buffer():
    with open(TXT_FILE, "rb") as f:
        c_generator = _count_generator(f.raw.read)
        data = [buffer.decode("utf-8").split("\n\n") for buffer in c_generator]
        data = [[int(z) for z in y.split("\n")] for x in data for y in x]
    return data


def groupby_read():
    with open(TXT_FILE, "r") as f:
        data = (k.split() for k in f.read().splitlines())

    final = []
    for _, v in groupby(data, lambda x: x != []):
        bb = list(v)
        if bb != [[]]:
            final.append([le(k[0]) for k in bb])
    return final


# cProfile.run("numpy_read()")
# cProfile.run("list_read_util()")
cProfile.run("list_read()")  # fastest
cProfile.run("list_read_buffer()")
# cProfile.run("groupby_read()")
