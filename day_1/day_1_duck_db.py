from typing import List

import duckdb


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


# to start an in-memory database
conn = duckdb.connect(database=":memory:")

# create a table with two integer columns
conn.execute("CREATE TABLE calories(elf INTEGER, calories INTEGER);")

txt_file: str = "./data/data_1.txt"
raw_data: List[List[int]] = list_read_buffer(txt_file)

final_data: List[List[int]] = [[i, y] for i, x in enumerate(raw_data) for y in x]

with open("./data/data_1.csv", "w") as fd:
    for item in final_data:
        write_str: str = "|".join([str(x) for x in item]) + "\n"
        fd.write(write_str)

# read a CSV file into a table
conn.execute("COPY calories FROM './data/data_1.csv' ( DELIMITER '|');")

# max calories for a single elf
print(
    conn.execute(
        """
    WITH sum_calories
    AS (
        SELECT elf, 
        sum(calories) total_calories
        FROM calories 
        group by elf)
    SELECT max(total_calories)
    FROM sum_calories
    ;"""
    ).fetchall()
)


# sum of the calories of the top 3 elves
print(
    conn.execute(
        """
    WITH sum_calories
    AS (
        SELECT elf, 
        sum(calories) total_calories
        FROM calories 
        group by elf
        order by total_calories desc
        limit 3)
    SELECT sum(total_calories)
    FROM sum_calories
    ;"""
    ).fetchall()
)
