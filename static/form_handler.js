category_select = document.querySelector('select#category')

edit_category_select = document.querySelector('select#category')

if (category_select != null) {
    selector = category_select
} else if (edit_category_select != null) {
    selector = edit_category_select
}

// following piece of code is used on pages of product creation and editing to load and display characteristics of a chosen category
if (selector != null) {
    selector.onchange = function() {
        category = selector.value

        fetch('/categories/get_characteristics/'+category+'/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8'
                    }
        }).then(function(response) {
            response.json().then(function(data) {
                // response is received here
                form = $("#product-form")
                // remove all old inputs which may have been left from the category chosen before
                $(".additional-input").remove();
                if (data.length != 0) {
                    $("<div class='additional-input'><b>Fill in product's characteristics</b></div>").appendTo(form)
                }
                //  and then inputs are displayed with a data received
                for (element of data) {
                    $("<div class='form-group additional-input'> <label class='control-label'>"+element[0]+"</label><input class='form-control' name='"+element[1]+"' type='text' placeholder='"+element[2]+"' value=''></div>").appendTo(form);
                }

            });
        });
    }
}
