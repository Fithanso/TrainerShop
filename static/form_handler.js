category_select = document.getElementById("add_product_category")

// following piece of code is used on the product addition page to load and display characteristics of a chosen category
if (category_select != null) {
    category_select.onchange = function() {
        category = category_select.value

        fetch('/categories/get_characteristics/'+category, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8'
                    }
        }).then(function(response) {
            response.json().then(function(data) {
                form = $("#add-product-form")
                $(".additional-input").remove();
                if (data.length != 0) {
                    $("<br>").appendTo(form)
                    $("<br>").appendTo(form)
                    $("<div class='additional-input'><b>Fill in product's characteristics</b></div>").appendTo(form)
                }
                for (element of data) {
                    $("<div class='form-group additional-input'> <label class='control-label'>"+element[0]+"</label><input class='form-control' name='"+element[1]+"' type='text' placeholder='"+element[2]+"' value=''></div>").appendTo(form);
                }

            });
        });
    }
}

