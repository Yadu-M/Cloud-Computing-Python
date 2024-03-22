import random
from hashlib import sha256
import random
import requests
import json

def generate_map_grid(row=None, col=None, noChange=True) -> list[list[int]]:    
    if noChange:
        try:
            f = open('map.txt', 'r')
            if ((f == None) or (len(f.readline()) == 0)):
                raise Exception
            else:
                return fetch_map_info()           
        
        except:              
    
            if row == None:
                row = random.randint(3, 10)
            if col == None:
                col = random.randint(3, 10)


            grid = []
            
            for i in range(row):
                curr_row = []
                for _ in range(col):            
                    if random.randint(1, 10) < 3:
                        curr_row.append(1)
                    else:
                        curr_row.append(0)
                grid.append(curr_row)
            
            
            generate_text_map(grid)
    
    else:
        if row == None:
                row = random.randint(3, 10)
        if col == None:
            col = random.randint(3, 10)


        grid = []
        
        for i in range(row):
            curr_row = []
            for _ in range(col):            
                if random.randint(1, 10) < 3:
                    curr_row.append(1)
                else:
                    curr_row.append(0)
            grid.append(curr_row)
        
        
        generate_text_map(grid)
    return fetch_map_info()



def generate_text_map(grid: list[list[int]]):
    
    with open(f'map.txt', 'w') as f:
        f.write(f'{len(grid)} {len(grid[0])}\n')
        i = 0
        j = 0
        for row in grid:
            i += 1
            for col in row:
                f.write(str (col))
                j += 1
                if (j < len(row)):
                    f.write(' ')
            if (i == len(grid)):
                break
            f.write('\n')
            j = 0
                
 
def fetch_map_info() -> list[list[int]]:   
    with open('map.txt', 'r') as f:
        x = f.readline()
        grid = []
        row = []
        while(len(x) != 0):
            if (x == '\n'):
                grid.append(row)
                row = []
            elif (x == '0'):  
                row.append(0)            
            elif (x == '1'):
                row.append(1)
            x = f.read(1)
        grid.append(row)
    return grid



def generate_mines_txt(map: list[list[int]]) -> list[list]:
    serial_num_list = random.sample(range(1000, 10000), (len(map) * len(map[0])))
    mine_list = []
    f = open('mines.txt', 'w')
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j]:
                serial_num = serial_num_list.pop()
                f.write(f'{i} {j} {serial_num}\n')
                mine_list.append([i, j, serial_num])
    f.close()
    return mine_list


def get_rover_commands(rover_id):
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