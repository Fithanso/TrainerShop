add_product_category_select = document.querySelector('select#add_category_select')

edit_product_category_select = document.querySelector('select#edit_category_select')

// following piece of code is used on the page of product editing to load and display characteristics of a chosen category with certain values from the product
if (edit_product_category_select != null) {
    edit_product_category_select.onchange = function() {
        category = edit_product_category_select.value
        product_id =  document.querySelector('input#product_id').value

        fetch('/categories/get_characteristics_values/'+category+'/'+product_id+'/', {
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
                    $("<div class='form-group additional-input'> <label class='control-label'>"+element["charc_name"]+"</label><input class='form-control' name='"+element["charc_id"]+"' type='text' placeholder='"+element["charc_type"]+"' value='"+element["value"]+"'></div>").appendTo(form);
                }

            });
        });
    }
}


// following piece of code is used on the page of product creation to load and display characteristics of a chosen category
if (add_product_category_select != null) {
    add_product_category_select.onchange = function() {
        category = add_product_category_select.value

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
                    $("<div class='form-group additional-input'> <label class='control-label'>"+element["charc_name"]+"</label><input class='form-control' name='"+element["charc_id"]+"' type='text' placeholder='"+element["charc_type"]+"' value=''></div>").appendTo(form);
                }

            });
        });
    }
}
