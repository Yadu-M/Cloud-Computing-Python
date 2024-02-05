from hashlib import sha256
import random
from map import mine_check


def disarm_mine(row: int, col: int, mine_list: list):
    for mine_info in mine_list:
        mine_info = mine_info.split()
        if row == int(mine_info[0]) and col == int(mine_info[1]):
            solved = False
            i = 0
            while not solved:
                serial_num = str(mine_info[2] + f'{i}')
                hashed_data = sha256(serial_num.encode()).hexdigest()
                if hashed_data[0:6] == '000000':
                    solved = True
                    print(f' disarmed mine at ({row - 1}, {int(col/2)}) \nHash: {hashed_data}, Serial Num: {serial_num}'
                          f', Pin: {i}, Temp Mine Key: {i}{serial_num}')

                i += 1
            return


def get_mines_location(row, col):
    location_list = []
    for i in range(row):
        for j in range(col):
            if mine_check(i + 1, j * 2):
                # print(j * 2)
                location_list.append((i + 1, j * 2))
            # if f.read(1) == "1":
            #     location_list.append((i, j))

    return location_list


def generate_mines_txt(row, col):
    mine_info_list = []
    mine_list = get_mines_location(row, col)
    f = open("mines.txt", "w")
    serial_num_list = random.sample(range(1000, 10000), len(mine_list))

    for row, col in mine_list:
        serial_num = serial_num_list.pop()
        f.write(f'{row - 1} {int(col/2)} {serial_num}\n')
        mine_info_list.append(f'{row} {col} {serial_num}')

    f.close()

    return mine_info_list
