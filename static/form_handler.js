
function get_form_data(e) {
    var arr = new Map();
    for (input of $(e).parent().find('input')) {
        arr.set($(input).attr('id'), $(input).val())
    }
    return Object.fromEntries(arr); // create json from map
}