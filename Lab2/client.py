import logging

import grpc
import proto_file_pb2
import proto_file_pb2_grpc

from map import create_rover_path, update_rover_path, mine_check
from mines import disarm_mine

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        
        stub = proto_file_pb2_grpc.MyGreeterStub(channel)        
        
        # Fetching map
        response = stub.GetMap(proto_file_pb2.Empty())
        grid = response.map_row
        
        MAP_ROW_SIZE = response.row
        MAP_COL_SIZE = response.col
        
        # for row in grid:
        #     for val in row.mine_val:
        #         print(val, end=" ")
        #     print()
            
        
        # Getting rover id from user        
        rover_id = 0        
        
        while True:
            try:
                rover_id = input('Enter rover id (Between or including 1-10): ')
                if ((int (rover_id) > 10) or (int (rover_id) < 1)):
                    raise ValueError
                break
            except ValueError:
                pass
        
        
        request = proto_file_pb2.RoverID(id=rover_id)        
        response = stub.GetCommands(request)
        rover_commands = response.commands
        
        
        # Executing map traversal
        # generate_rover_path(int (rover_id), rover_commands, row_size, col_size)
        dig = False
        curr_row = 1
        curr_col = 0
        direction_v = "SOUTH"
        fail = False
        create_rover_path(rover_id, MAP_ROW_SIZE, MAP_COL_SIZE)
        update_rover_path(rover_id, curr_row, curr_col)  # Initializing path
        for move in rover_commands:            
            if move == 'L' or move == 'R':
                direction_v = update_direction(direction_v, move)

            elif move == 'M':
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
                    if curr_row > 1:  
                        curr_row -= 1
                        update = True
                elif direction_v == "EAST":
                    if curr_col < ((MAP_COL_SIZE - 1) * 2):
                        curr_col += 2
                        update = True

                if update:
                    if not dig and mine_check(row_before, col_before, rover_id):                        
                        request = proto_file_pb2.BotMessage(_message=f'Rover {rover_id} exploded at row: {row_before - 1} col: {int(col_before/2)}')
                        response = stub.NotifyServer(request)                        
                        fail = True
                        break
                    dig = False
                    update_rover_path(rover_id, curr_row, curr_col)

            elif move == 'D':
                dig = True
                if mine_check(curr_row, curr_col, rover_id, disable=False):                    
                    request = proto_file_pb2.MineLocation(row=(curr_row - 1), col=(curr_col + 1))
                    response = stub.GetMineSerialNum(request)
                    
                    pin = disarm_mine(response.serialNum)
                    
                    request = proto_file_pb2.RoverInfo(
                        pin_num=str(pin),
                        rover_id=str(rover_id),
                        row=str(curr_row - 1),
                        col=str(int(curr_col/2))
                    )        
                    response = stub.MinePin(request)                    
                    mine_check(curr_row, curr_col, rover_id, disable=True)
        
        if not fail:  # Send success notification to
            request = proto_file_pb2.BotMessage(_message=f'Rover {rover_id} has successfully completed all commands.')
            response = stub.NotifyServer(request)   
                    

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
      
if __name__ == '__main__':
    logging.basicConfig()
    run()