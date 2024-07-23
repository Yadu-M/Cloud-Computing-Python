const base_url = 'http://127.0.0.1:8000'

export const get_map = async () => {

    try {
        const response = await fetch(`${base_url}/map`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
    
        return await response.json();

    } catch (error) {
        alert(error);
    }
}

export const get_commands = async (rover_id) => {

    try {
        const response = await fetch(`${base_url}/commands/${rover_id}`, );    
        return await response.json();

    } catch (error) {
        alert(error);
    }
}

export const create_rover = async (commands) => {
    try {
        const response = await fetch(`${base_url}/rovers?incoming_command=${commands}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            }
        });

        return await response.json();

    } catch (error) {
        alert(error);
    }
}


export const delete_rover = async (id) => {
    try {
        const response = await fetch(`${base_url}/rovers/${id}`, {
            method: "DELETE",
        });

        return await response.json();
    } catch (error) {
        alert(error);
    }
}


export const get_mines = async () => {
    try {
        const response = await fetch(`${base_url}/mines`, {
            method: "GET",
        });

        return await response.json();
    } catch (error) {
        alert(error);
    }
}


export const disarm_mine = async (id) => {
    try {
        const response = await fetch(`${base_url}/mines/${id}`, {
            method: "GET",
        });

        return await response.json();
    } catch (error) {
        alert(error);
    }
}