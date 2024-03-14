import random

'''
Utility functions for edition text files
'''


def create_map(row, col):
    """
    Creates a random map based on the row and col
    :param row: Row size of map
    :param col: Col size of map
    :return:
    """
    with open('map.txt', 'w') as f:
        f.write(f'{row} {col}\n')
        for i in range(row):
            for j in range(col):
                if random.randint(1, 10) < 3:
                    f.write('1')
                else:
                    f.write('0')
                if j < (col - 1):
                    f.write(' ')
            if i < (row - 1):  # This removes extra line in the map
                f.write('\n')


def update_rover_path(rover_id, row, col):
    """
    Updates the rover path given the row and col    
    :param rover_id: Rover id
    :param row: Row to update
    :param col: Col to update
    :return:
    """
    rover_path = open(f'path_{rover_id}.txt', 'rb+')
    for i in range(row):  # Align file pointer to correct row
        next(rover_path)

    rover_path.seek(col, 1)  # Align file pointer to correct col
    rover_path.write(bytes('*', 'utf-8'))  # Marking rover path
    rover_path.close()


def mine_check(row, col, rover_id=None, disable=False):
    """
    Checks if mine exists map for the given row, col
    :param disable:
    :param rover_id:
    :param row: Row in the map
    :param col: Col in the map
    :return:
    """

    if rover_id is None:
        rover_map = open(f'map.txt', 'rb+')
    else:
        rover_map = open(f'map_{rover_id}.txt', 'rb+')

    for i in range(row):
        next(rover_map)

    rover_map.seek(col, 1)

    if rover_map.read(1).decode('utf-8') == '1':  # Checking for mine
        if disable:
            rover_map.seek(-1, 1)  # Move the pointer 1 back to reset
            rover_map.write(bytes('X', 'utf-8'))  # Mark mine as X (for now)
        rover_map.close()
        return True

    rover_map.close()
    return False


def create_rover_path(rover_id, rows, cols):
    """
    Initializes the map for each rover
    :param rover_id:  id
    :param rows: Total number of rows
    :param cols: Total number of cols
    :return:
    """
    with open(f'path_{rover_id}.txt', 'w') as f:
        f.write('\n')
        for i in range(rows):
            for j in range(cols):
                f.write('0')
                if j < (cols - 1):
                    f.write(' ')
            if i < (rows - 1):  # This removes extra line in the map
                f.write('\n')


def fetch_map_size(map_file_name) -> tuple:
    fmap = open(map_file_name, 'r')
    size = fmap.readline().split()
    fmap.close()
    return int(size[0]), int(size[1])


def generate_maps(rover_id, rows):
    with open(f'map_{rover_id}.txt', 'w') as f, open('map.txt', 'r') as m:
        for i in range(rows + 1):
            f.write(m.readline())
