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
        throw new Error("Something went wrong while fetching map data");
    }
}

export const get_commands = async (rover_id) => {

    try {
        const response = await fetch(`${base_url}/commands/${rover_id}`, );    
        return await response.json();

    } catch (error) {
        throw new Error("Something went wrong while fetching commands");
    }
}

export const create_rover = async () => {
    try {
        const response = await fetch(`${base_url}/rovers`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            body: {

            }
        });
    } catch (error) {
        
    }
}
