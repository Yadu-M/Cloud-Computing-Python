import requests
import json
from map import create_map, update_rover_path, create_rover_path, mine_check

MAP_ROW_SIZE = 50
MAP_COL_SIZE = 50


def main():

    create_map(MAP_ROW_SIZE, MAP_COL_SIZE)

    for rover_id in range(1, 11):
        rover_data = get_rover_commands(rover_id)
        if mine_check(1, 0):
            if rover_data['data']['moves'][0] != 'D':
                print(f'bot{rover_id} explodes at (0, 0)')
                continue

        prev_move = ''
        curr_row = 1
        curr_col = 0
        create_rover_path(rover_id, MAP_ROW_SIZE, MAP_COL_SIZE)
        update_rover_path(rover_id, 1, 0)
        for move in rover_data['data']['moves']:
            if prev_move != 'D' and mine_check(curr_row, curr_col):
                print(f'bot{rover_id} explodes at ({curr_row - 1}, {curr_col})')
                break

            if move == 'L':
                if curr_col != 0:
                    curr_col -= 1

            elif move == 'R':
                if curr_col != (MAP_COL_SIZE - 1):
                    curr_col += 1

            elif move == 'M':
                if curr_row != (MAP_ROW_SIZE - 1):
                    curr_row += 1

            update_rover_path(rover_id, curr_row, curr_col)
            prev_move = move


def get_rover_commands(rover_id):
    api = 'https://coe892.reev.dev/lab1/rover'
    r = requests.get(f'{api}/{rover_id}')
    if r.ok:
        content = json.loads(r.content)
        return content
    else:
        raise Exception("Failed to fetch api")


if __name__ == "__main__":
    main()
