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
            if i == (row - 1):  # This removes extra line in the map
                break
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
        rover_path.readline()

    rover_path.seek(col, 1)  # Align file pointer to correct col
    rover_path.write(bytes('*', 'utf-8'))  # Marking rover path
    rover_path.close()
    return True


def mine_check(row, col):
    """
    Checks if mine exists map for the given row, col
    :param row: Row in the map
    :param col: Col in the map
    :return:
    """
    rover_map = open('map.txt', 'rb+')

    for i in range(row):
        rover_map.readline()

    rover_map.seek(col, 1)

    if rover_map.read(1).decode('utf-8') == '1':  # Checking for mine
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
            if i == (rows - 1):  # This removes extra line in the map
                break
            f.write('\n')
