from fastapi import FastAPI, status, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


import utils
import random

# Rover statuses
NOT_STARTED = "NOT_STARTED"
FINISHED = "FINISHED"
MOVING = "MOVING"
ELIMINATED = "ELIMINATED"

app = FastAPI()

origins = [
    "http://localhost.*",
    "https://localhost/*",
    "http://localhost:80",
    "http://localhost:8080",
    "http://localhost:8000",
    "https://coe892lab42024g.azurewebsites.net/*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="dist", html=True), name="static")

# Set up the Jinja2 templates directory
templates = Jinja2Templates(directory="/app/dist")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Map/Mine/Rover data
grid, mines = utils.generate_map_grid(row=10, col=10)
rovers = []
commands = [utils.get_rover_commands(id) for id in range(1, 11)]
id_list = random.sample(range(100, 1000), 900)
valid_commands = ['L', 'R', 'M', 'D']

# print(grid, mines)


# General Data structs
class MapDimensions(BaseModel):
    row: int
    col: int


class Mine(BaseModel):
    row: int
    col: int
    serialNum: int


@app.get("/map", status_code=status.HTTP_200_OK)
def get_map():
    global grid, mines
    grid, mines = utils.generate_map_grid(row=10, col=10)
    grid[0][0] = 0
    return {
        "row": len(grid),
        "col": len(grid[0]),
        "map": grid
    }


@app.put("/map")
def update_map(item: MapDimensions, status_code=status.HTTP_201_CREATED):
    global grid, mines
    grid, mines = utils.generate_map_grid(row=item.row, col=item.col)
    grid[0][0] = 0
    # print(f'Map has been updated with new height and width:\n{grid}')
    # print(f'New row: {len(grid)}')
    # print(f'New col: {len(grid[0])}')
    # print(f'New mines: {mines}')
    return status_code


# --------------------------------Endpoints for Mines------------------------------#

@app.get("/mines")
def get_mines():
    mines_dict = [{"row": info[0], "col": info[1], "id": info[2]} for info in mines]
    return mines_dict


@app.get("/mines/{id}")
def get_mine_id(id: int):
    for info in mines:
        if info[2] == id:
            return utils.disarm_mine(str(id))
    raise HTTPException(status_code=404, detail="Mine with serial num not found")


@app.delete("/mines/{id}")
def delete_mine(id: int):
    global mines
    for i, info in enumerate(mines):
        if info[2] == id:
            row = info[0]
            col = info[1]

            grid[row][col] = 0

            for j, [row_, col_, _] in enumerate(mines):
                if row == row_ and col == col_:
                    mines.pop(j)

            # print(f'Mine deleted')
            return

    raise HTTPException(status_code=404, detail="Mine with serial num not found")


@app.post("/mines")
def create_mine(new_mine: Mine):
    if grid[new_mine.row][new_mine.col]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mine already exists at the given location")
    grid[new_mine.row][new_mine.col] = 1
    mines.append([new_mine.row, new_mine.col, new_mine.serialNum])
    return {
        "id": "ID OF MINE"
    }


@app.get("/rovers")
def get_rovers():
    return rovers


@app.get("/rovers/{id}")
def get_rover_id(id: int):
    for rover_id, commands, status, position in rovers:
        if id == rover_id:
            # print(f'Successfully found the rover')
            return {"id": rover_id,
                    "status": status,
                    "commands": commands,
                    "position": position}


@app.post("/rovers")
def create_rover(incoming_command: str):
    incoming_command = incoming_command.upper()
    for command in incoming_command:
        if command not in valid_commands:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid command found in command list,"
                                                                                "Must be \"L\", \"R\", \"M\", \"D\""                                                                            
                                                                                "")
    rovers.append({"id": id_list.pop(), "commands": incoming_command, "status": NOT_STARTED, "position": (0, 0)})
    return rovers[len(rovers) - 1]["id"]


@app.delete("/rovers/{id}")
def delete_rover(id: int):
    for i, rover in enumerate(rovers):
        if id == rover['id']:
            rovers.pop(i)
            return

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Rover with id {id} not found')


@app.get("/commands/{id}")
def get_commands(id: int):
    return utils.get_rover_commands(id)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}
