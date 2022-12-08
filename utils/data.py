from typing import List


def read_text_file_to_list(file: str) -> List[str]:
    with open(file, "r") as f:
        data: List[str] = []
        for ele in f:
            data.append(ele)

    return data
