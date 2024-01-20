import random

"""
Map function
"""


def create_map(row, col):
    with open('map.txt', 'w') as f:
        f.write(f'{row} {col}\n')
        for i in range(row):
            for j in range(col):
                if random.randint(1, 10) < 3:
                    f.write('1')
                else:
                    f.write('0')
            if i == (row - 1):  # This removes extra line in the map
                break
            f.write('\n')


def update_rover_path(rover_id, row, col):

    rover_path = open(f'path_{rover_id}.txt', 'rb+')

    # rover_path.seek(0, 0)
    # print(curr_row)
    for i in range(row):
        rover_path.readline()

    rover_path.seek(col, 1)
    rover_path.write(bytes('*', 'utf-8'))
    rover_path.close()
    return True


def mine_check(row, col):
    rover_map = open('map.txt', 'rb+')

    for i in range(row):
        rover_map.readline()

    rover_map.seek(col, 1)

    if rover_map.read(1).decode('utf-8') == '1':
        rover_map.seek(-1, 1)
        rover_map.write(bytes('X', 'utf-8'))
        rover_map.close()
        return True

    rover_map.close()
    return False


def create_rover_path(rover_id, rows, cols):
    with open(f'path_{rover_id}.txt', 'w') as f:
        f.write('\n')
        for i in range(rows):
            for j in range(cols):
                f.write('0')
            if i == (rows - 1):  # This removes extra line in the map
                break
            f.write('\n')
