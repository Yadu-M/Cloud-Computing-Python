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