import { create_rover, delete_rover, get_commands, get_map } from './api_calls';

export const clear_div = (div) => {
    const div_to_clear = document.querySelector(`.${div}`);
    while (div_to_clear.firstChild)
        div_to_clear.removeChild(div_to_clear.firstChild);
}

export const clear_by_id = (id) => {
    const elem_to_clear = document.getElementById(id);
    while (elem_to_clear.firstChild)
        elem_to_clear.removeChild(elem_to_clear.firstChild);
}


export async function list_commands(rover_id) {
    const elem_to_clear = document.getElementById('commands')
    if (elem_to_clear !== null)
        elem_to_clear.remove();

    const commands_elem = document.createElement("h4");
    commands_elem.id = "commands";
    let commands = await get_commands(rover_id);

    commands_elem.innerText = `Commands: ${commands}`;
    document.getElementById('commandForm').appendChild(commands_elem);    
    
    return commands;
    
}

export async function generate_map() {
    
    const map = document.getElementById("map");
    const map_obj = await get_map();

    map_obj.map.forEach((row, i) => {

        const row_html = document.createElement("div");
        row_html.className = "row";

        row.forEach((value, j) => {
            const cell = document.createElement("div");
            let className = "cell";
            if (value === 1) 
                className += " mine";
            cell.className = className;
            cell.title = `(${(i + 1)} , ${(j + 1)})`;
            cell.setAttribute("id", `${i}-${(j)}`)

            row_html.appendChild(cell);
        });

        map.appendChild(row_html);
        
    });

    return map_obj;
}


export async function add_rover(commands) {
    const response = await create_rover(commands);
    const rover_elem = document.getElementById("rover");
    rover_elem.innerText = `Rover Id: ${response}`;
    return response;
}


export function update_cell_color(row, col, color='green') {
    const cell_to_update = document.getElementById(`${row}-${col}`);
    cell_to_update.style.backgroundColor = color;
}

export function update_cell(row, col, move_num, color='green') {
    const cell_to_update = document.getElementById(`${row}-${col}`);
    cell_to_update.innerText += move_num + ", ";
    cell_to_update.style.backgroundColor = color;
}

export function remove_comma(row, col, move_num, color='green') {
    const cell_to_update = document.getElementById(`${row}-${col}`);
    cell_to_update.innerText += move_num;
    cell_to_update.style.backgroundColor = color;
}

export async function cleanup(rover_id) {
    clear_div('map');
    clear_by_id('rover');    
    clear_by_id('info');
    await delete_rover(rover_id);

}

export function update_direction(curr_direction, move) {
    if (curr_direction === "NORTH") {
        if (move === "L") {
            return "WEST";
        } else {
            return "EAST";
        }
    } else if (curr_direction === "WEST") {
        if (move === "L") {
            return "SOUTH";
        } else {
            return "NORTH";
        }
    } else if (curr_direction === "SOUTH") {
        if (move === "L") {
            return "EAST";
        } else {
            return "WEST";
        }
    } else if (curr_direction === "EAST") {
        if (move === "L") {
            return "NORTH";
        } else {
            return "SOUTH";
        }
    }
}


