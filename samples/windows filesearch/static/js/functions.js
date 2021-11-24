function emptyOutFilter(selectBox) {
    selectBox = document.getElementById(selectBox);
    selectBox.options.length = 0;


}

function remove(array, element) {
    return array.filter(el => el !== element);
}

function detectKeyboardEnter(event) {
    var key_board_keycode = event.which || event.keyCode;
    if (key_board_keycode == 13) {
        event.preventDefault();
        myFunction();
    }
}



function clickToCopy(cellValue) {
    // cellValue.select();
    var test = $('<input>').val(cellValue).appendTo('body').select();
    document.execCommand("copy");

    // alert("Path copied");





}