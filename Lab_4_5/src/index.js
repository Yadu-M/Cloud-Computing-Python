import _ from 'lodash';
import './styles/styles.css'
import { list_commands, generate_map, add_rover, cleanup, update_direction, update_cell, update_cell_color } from './scripts/utils';
import { get_mines, disarm_mine } from './scripts/api_calls';

const command_form = document.getElementById("commandForm");
const start_btn = document.getElementById("start");
const info_elem = document.getElementById("info");
const map_elem = document.getElementById("map");

let is_map_compiled = false;

let command_id = null;
let rover_id = null;
let commands = "";
let begin = false;
let map_obj = {};
let mines_list = [];
let disarmed_mines_list = []

command_form.addEventListener("submit", async event => {
    event.preventDefault();
    const commands_elem = document.getElementById("input-commands");
    command_id = commands_elem.value;
    if (isNaN(command_id) || command_id < 1 || command_id > 10) {
        alert("Enter an id between 1 and 10");
    }
    else {     
        if (is_map_compiled === true) {
            await cleanup(rover_id);
        }
        await init();
        is_map_compiled = true;
    }

})


start_btn.addEventListener("click", async e => {
    e.preventDefault();
    if (begin == true) await begin_exploration();
    else alert('Please generate commands above');
})

async function init() {
    try {

        commands = await list_commands(command_id);
        map_obj = await generate_map();
        rover_id = await add_rover(commands);
        mines_list = await get_mines();
        begin = true;

        
        const mines_count_elem = document.createElement("h4");
        mines_count_elem.innerText = `Total mines count: ${mines_list.length}`
        info_elem.appendChild(mines_count_elem);

        mines_count_elem.textContent = `Total mine count: ${mines_list.length}`
    } catch (error) {
        alert('Something went wrong: ', error);
    }
}



async function begin_exploration() {
    let curr_row = 0;
    let curr_col = 0;
    let curr_direction = 'SOUTH';
    const max_row_size = map_obj.row;
    const max_col_size = map_obj.col;
    const map = map_obj.map;
    let move_num = 0
    update_cell(curr_row, curr_col, move_num);
    
    for (let i = 0; i < commands.length; i++) {
        if (commands.at(i) === 'L' || commands.at(i) === 'R') {
            curr_direction = update_direction(curr_direction, commands.at(i));
        }
        else if (commands.at(i) === 'M') {
            let update = false;

            if (curr_direction === "SOUTH") {
                if (curr_row < (max_row_size - 1)) {
                    curr_row += 1;
                    update = true;
                }
            } else if (curr_direction === "WEST") {
                if (curr_col > 0) {
                    curr_col -= 1;
                    update = true;
                }
            } else if (curr_direction === "NORTH") {
                if (curr_row > 0) {
                    curr_row -= 1;
                    update = true;
                }
            } else if (curr_direction === "EAST") {
                if (curr_col < (max_col_size - 1)) {
                    curr_col += 1;
                    update = true;
                }
            }

            if (update === true) {
                move_num ++;
                if (map[curr_row][curr_col] === 1) {
                    for (const mine of mines_list) {
                        if (mine.row === curr_row && mine.col === curr_col) {    
                            disarmed_mines_list.push([curr_row, curr_col]);     

                            const key = await disarm_mine(mine.id);
                            const disarm_mine_elem = document.createElement("h4");
                            disarm_mine_elem.textContent = `Disarmed mine at (${curr_row}, ${curr_col}) with key: ${key}`
                            info_elem.appendChild(disarm_mine_elem);
                            update_cell(curr_row, curr_col, move_num, 'orange');
                            map[curr_row][curr_col] = 0;

                            break;
                        }                      
                    }

                }
                else
                    update_cell(curr_row, curr_col, move_num);

            }            
            
        }

    }

    for (const item of disarmed_mines_list) {
        update_cell_color(item[0], item[1], 'orange');
    }

    for (const row of map_elem.children) {
        for (const cell of row.children) {
            cell.textContent = cell.textContent.substring(0, cell.textContent.length - 2);
        }
    }

    alert('Done');

}