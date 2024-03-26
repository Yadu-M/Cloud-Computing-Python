from typing import Union

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import utils

# Rover statuses
NOT_STARTED = "NOT_STARTED"
FINISHED = "FINISHED"
MOVING = "MOVING"
ELIMINATED = "ELIMINATED"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_methods='*',
    allow_headers='*',
    allow_credentials=True
)

# Map/Mine/Rover data
grid = utils.generate_map_grid(row=10, col=10)
mines = utils.generate_mines_txt(grid)
rovers = [{"id": 0, "commands": "", "status": "", "position": (0, 0)} for _ in range(10)]
commands = [utils.get_rover_commands(id) for id in range(1, 11)]


# General Data structs
class MapDimensions(BaseModel):
    row: int
    col: int


class Mine(BaseModel):
    row: int
    col: int
    serialNum: int


# ------End point definitions----#

@app.get("/")
def read_root():
    return {""}


# --------------------------------Endpoints for Map--------------------------------#

@app.get("/map", status_code=status.HTTP_200_OK)
def get_map():
    return {
        "row": len(grid),
        "col": len(grid[0]),
        "map": grid
    }


@app.put("/map")
def update_map(item: MapDimensions, status_code=status.HTTP_201_CREATED):
    global grid, mines
    grid, mines = utils.generate_map_grid(row=item.row, col=item.col, no_change=False)
    print(f'Map has been updated with new height and width:\n{grid}')
    print(f'New row: {len(grid)}')
    print(f'New col: {len(grid[0])}')
    print(f'New mines: {mines}')
    return status_code


# --------------------------------Endpoints for Mines------------------------------#

@app.get("/mines")
def get_mines():
    mines_dict = [{"row": info[0], "col": info[1], "id": info[2]} for info in mines]
    return mines_dict


@app.get("/mines/{id}")
def get_mines_id(id: int):
    for info in mines:
        if info[2] == id:
            return {"row": info[0], "col": info[1], "id": info[2]}

    raise HTTPException(status_code=404, detail="Mine with serial num not found")


@app.delete("/mines/{id}")
def delete_mine(id: int):
    global mines
    for i, info in enumerate(mines):
        if info[2] == id:
            row = info[0]
            col = info[1]

            grid[row][col] = 0
            mines.pop(i)
            utils.remove_mine(" ".join(str(item) for item in info), grid)
            print(f'Mine deleted')
            return

    raise HTTPException(status_code=404, detail="Mine with serial num not found")


@app.post("/mines")
def create_mine(new_mine: Mine):
    if grid[new_mine.row][new_mine.col]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mine already exists at the given location")
    grid[new_mine.row][new_mine.col] = 1
    utils.generate_text_map(grid)
    mines.append([new_mine.row, new_mine.col, new_mine.serialNum])
    utils.add_mine(f'{new_mine.row} {new_mine.col} {new_mine.serialNum}', grid)
    return {
        "id": "ID OF MINE"
    }


# @app.put("/mines/{id}")
# def update_mine(id: int, new_mine: Mine | None):
#     for info in mines:
#         if info.:


# --------------------------------Endpoints for Rover------------------------------#

@app.get("/rovers")
def get_rovers():
    return rovers


@app.get("/rovers/{id}")
def get_rover_id(rover_id: int):
    for id, commands, status, position in rovers:
        if id == rover_id:
            print(f'Successfully found the rover')
            return {"id": rover_id,
                    "status": status,
                    "commands": commands,
                    "position": position}


@app.post("/rovers")
def create_rover(incoming_command: str):
    for i, command in enumerate(commands):
        if command == incoming_command:
            rovers.append({"id": i + 1, "commands": incoming_command, "status": NOT_STARTED, "position": (0, 0)})
            return {"id": i + 1}


@app.delete("/rovers/{id}")
def delete_rover(rover_id: int, id: int):
    for id in rovers:
        if id == rover_id:
            rovers.pop(id - 1)
            return

        # @app.put("/rovers/{id}")


# def update_command()

@app.get("/commands/{id}")
def get_commands(id: int):
    return utils.get_rover_commands(id)


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
#

