import requests
import json
from time import perf_counter
from threading import Thread
from map import create_map, update_rover_path, create_rover_path, mine_check

MAP_ROW_SIZE = 7
MAP_COL_SIZE = 7


def main():
    create_map(MAP_ROW_SIZE, MAP_COL_SIZE)

    time1 = single_thread()
    time2 = multi_thread()
    print(f'The difference is {round(abs(time1 - time2), 2)}')


def single_thread():
    start_time = perf_counter()
    generate_rover_paths()
    end_time = perf_counter()
    print(f'Single threaded approach took {end_time - start_time: 0.2f} second(s) to complete.')
    return end_time - start_time


def multi_thread():
    thread_list = []
    start_time = perf_counter()

    for rover_id in range(1, 11):
        thread_list.append(Thread(target=generate_rover_path, args=(rover_id, )))

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    end_time = perf_counter()
    print(f'Multi Threaded approach took {end_time - start_time: 0.2f} second(s) to complete.')
    return end_time - start_time


def generate_rover_paths():
    """
    Generates all the rover paths
    :return: None
    """
    for rover_id in range(1, 11):  # 10 grabbing all 10 rover commands
        generate_rover_path(rover_id)


def generate_rover_path(rover_id):
    rover_commands = get_rover_commands(rover_id)
    prev_move = rover_commands[0]  # Initializing move
    curr_row = 1
    curr_col = 0
    create_rover_path(rover_id, MAP_ROW_SIZE, MAP_COL_SIZE)
    update_rover_path(rover_id, curr_row, curr_col)  # Initializing path
    for move in rover_commands:
        if prev_move != 'D' and mine_check(curr_row, curr_col):
            # print(f'Rover {rover_id} exploded at ({curr_row}, {curr_col})')
            break

        if move == 'M':
            if curr_row < MAP_ROW_SIZE:
                curr_row += 1

        elif move == 'L':
            if curr_col != 0:
                curr_col -= 2

        elif move == 'R':
            if curr_col < ((MAP_COL_SIZE - 1) * 2):
                curr_col += 2

        update_rover_path(rover_id, curr_row, curr_col)
        prev_move = move


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


if __name__ == "__main__":
    main()
