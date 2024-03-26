// import { test } from "./test";
import _ from 'lodash';
import './styles/styles.css'
import { get_commands, get_map } from './scripts/api_calls';
import { clear_by_id, clear_div } from './scripts/utils';

const base_url = 'http://127.0.0.1:8000';

const rover_form = document.getElementById("roverForm");

// let allow_submission = true;
// let prev_id = 0;
let is_map_compiled = false;
rover_form.addEventListener("submit", (event) => {
    event.preventDefault();
    const rover_id_elem = document.getElementById("roverId");
    const rover_id = rover_id_elem.value;
    rover_id;
    if (isNaN(rover_id) || rover_id < 1 || rover_id > 10) {
        alert("Enter an id between 1 and 10");
    }
    else {        
        if (is_map_compiled === true)
            clear_div('map');
        init(rover_id);
        is_map_compiled = true;
    }

})

async function init(rover_id) {
    await list_commands(rover_id);
    await generate_map(rover_id);
}


async function list_commands(rover_id) {
    const elem_to_clear = document.getElementById('commands')
    if (elem_to_clear !== null)
        elem_to_clear.remove();

    const commands_elem = document.createElement("h4");
    commands_elem.id = "commands";
    const commands = await get_commands(rover_id);

    commands_elem.innerText = `Commands: ${commands}`;
    document.getElementById('roverForm').appendChild(commands_elem);    
    
}

async function generate_map(id) {
    
    const map = document.getElementById("map");
    const map_obj = await get_map();


    // // Iterating through the map rows

    map_obj.map.forEach((row, i) => {

        // console.log(row);
        const row_html = document.createElement("div");
        row_html.className = "row";
        // row_html.title = `row${i + 1}`;

        row.forEach((value, j) => {
            const cell = document.createElement("div");
            let className = "cell";
            if (value === 1) 
                className += " mine";
            cell.className = className;
            cell.textContent = value;
            // console.log(i, j);
            cell.title = `(${(i + 1)} , ${(j + 1)})`;
            row_html.appendChild(cell);
        });

        map.appendChild(row_html);
        
    });
}




