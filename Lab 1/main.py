import requests
import json
from time import perf_counter
from threading import Thread
from map import create_map, update_rover_path, create_rover_path, mine_check, fetch_map_size, generate_maps
from mines import disarm_mine, generate_mines_txt

MAP_ROW_SIZE = 0
MAP_COL_SIZE = 0

ROVER_COMMANDS = []
MINES_LIST = []


def main():
    # create_map(10, 10)
    row_count, col_count = fetch_map_size("map.txt")
    # print(row_count, col_count)
    global MAP_ROW_SIZE
    global MAP_COL_SIZE
    MAP_ROW_SIZE = row_count
    MAP_COL_SIZE = col_count
    commands = []

    global ROVER_COMMANDS
    ROVER_COMMANDS = commands  # fetching commands

    #  Generating mines.txt
    global MINES_LIST
    MINES_LIST = generate_mines_txt(MAP_ROW_SIZE, MAP_COL_SIZE)
    # print(MINES_LIST)

    for rover_id in range(1, 11):
        create_rover_path(rover_id, MAP_ROW_SIZE, MAP_COL_SIZE)
        commands.append(get_rover_commands(rover_id))
        generate_maps(rover_id, MAP_ROW_SIZE)

    generate_rover_paths()
    
    # time1 = single_thread()

    # for rover_id in range(1, 11):
    #     create_rover_path(rover_id, MAP_ROW_SIZE, MAP_COL_SIZE)
    #     commands.append(get_rover_commands(rover_id))
    #     generate_maps(rover_id, MAP_ROW_SIZE)

    # time2 = multi_thread()
    # print(f'The difference is {round((time1 - time2), 3)} second(s)')


def single_thread():
    start_time = perf_counter()
    generate_rover_paths()
    end_time = perf_counter()
    print(f'Single threaded approach took {end_time - start_time: 0.3f} second(s) to complete.')
    return end_time - start_time


def multi_thread():
    thread_list = []
    start_time = perf_counter()

    for rover_id in range(0, 10):
        thread_list.append(Thread(target=generate_rover_path, args=(rover_id, )))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    end_time = perf_counter()
    print(f'Multi Threaded approach took {end_time - start_time: 0.3f} second(s) to complete.')
    return end_time - start_time


def generate_rover_paths():
    """
    Generates all the rover paths
    :return: None
    """
    for rover_id in range(0, 10):  # 10 grabbing all 10 rover commands
        generate_rover_path(rover_id)


def generate_rover_path(rover_id):

    dig = False
    curr_row = 1
    curr_col = 0
    direction_v = "SOUTH"
    update_rover_path(rover_id + 1, curr_row, curr_col)  # Initializing path
    total_time = 0
    for move in ROVER_COMMANDS[rover_id]:
        if move == 'L' or move == 'R':
            direction_v = update_direction(direction_v, move)

        elif move == 'M':
            # print(rover_id + 1, curr_row, curr_col, direction_v)
            update = False
            row_before = curr_row
            col_before = curr_col

            if direction_v == "SOUTH":
                if curr_row < MAP_ROW_SIZE:
                    curr_row += 1
                    update = True
            elif direction_v == "WEST":
                if curr_col >= 2:
                    curr_col -= 2
                    update = True
            elif direction_v == "NORTH":
                if curr_row > 1:  # Upper border
                    curr_row -= 1
                    update = True
            elif direction_v == "EAST":
                if curr_col < ((MAP_COL_SIZE - 1) * 2):
                    curr_col += 2
                    update = True

            if update:
                if not dig and mine_check(row_before, col_before, rover_id + 1):
                    print(f'Rover {rover_id + 1} exploded at ({row_before}, {col_before})')
                    break
                dig = False
                update_rover_path(rover_id + 1, curr_row, curr_col)

        elif move == 'D':
            dig = True
            if mine_check(curr_row, curr_col, rover_id + 1, disable=False):
                print(f'Rover {rover_id + 1}', end="")
                start_time = perf_counter()    
                disarm_mine(curr_row, curr_col, MINES_LIST)
                end_time = perf_counter()
                print(f'Finished disarming the mine in {round((end_time - start_time), 1)} seconds.\n')
                total_time += (end_time - start_time)
                mine_check(curr_row, curr_col, rover_id + 1, disable=True)
    
    print(f'Total time took: {total_time} seconds.')


def get_rover_commands(rover_id):
    """
    Function grabs the rover commands from the api
    :param rover_id: The rover id
    :return: Rover commands in JSON
    """
    api = 'https://coe892.reev.dev/lab1/rover'
    r = requests.get(f'{api}/{rover_id}')
    if r.ok:
        content = json.loads(r.content)
        return content['data']['moves']
    else:
        raise Exception("Failed to fetch api")


def update_direction(curr_direction, move) -> str:

    if curr_direction == "NORTH":
        if move == "L":
            return "WEST"
        else:
            return "EAST"

    elif curr_direction == "WEST":
        if move == "L":
            return "SOUTH"
        else:
            return "NORTH"

    if curr_direction == "SOUTH":
        if move == "L":
            return "EAST"
        else:
            return "WEST"

    if curr_direction == "EAST":
        if move == "L":
            return "NORTH"
        else:
            return "SOUTH"


if __name__ == "__main__":
    main()
