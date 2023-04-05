function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

    $(document).on('click','.show-products',function(event){
        console.log('ajax')
        var client_id = $('#id_client').val();
        console.log(client_id);
        const csrftoken = getCookie('csrftoken');
        if(typeof $('#id_client').val() != '') {
            event.preventDefault();
            $.ajax({
                type: 'POST',
                url: '/general/get-orders-from-client/' + client_id,
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                    'client_id': client_id,
                },
                success: function(response) {
                    for(var item in response) {
                        $('.orders-in-forms').html('');
                        html = '<button type="button" class="btn-primary product-list-button" data-id="' + response[item]['pk'] + '">' + response[item]['fields']['name'] + '</button>';
                        $('.orders-in-forms').append(html);
                    }
                }
            })
        }
    })

    $(document).on('change', '#id_client', function(event){
        event.preventDefault();
        $('.orders-in-forms').html('');
        var client_id = $('#id_client').val();
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: '/general/get-orders-from-client/' + client_id,
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'client_id': client_id,
            },
            success: function(response) {
                console.log(response);
                for(var item in response) {
                    html = '<button type="button" class="btn-primary product-list-button" data-id="' + response[item]['pk'] + '">' + response[item]['fields']['name'] + '</button>';
                    $('.orders-in-forms').append(html);
                }
            }
        })
    })

    $(document).on('click', '.product-list-button' ,function(event){
        event.preventDefault();
        $('#form-product-container').html('');
        const csrftoken = getCookie('csrftoken');
        if($(this).hasClass('product-list-button')) {
            $.ajax({
                type: 'POST',
                url: '/general/product-list-from-order/' + $(this).attr('data-id'),
                data: {
                'csrfmiddlewaretoken': csrftoken,
                'order_id': $(this).attr('data-id'),
            },
                success: function(response){
                    console.log(response);
                    html = response;
                    $('#form-product-container').append(html);
                }
            })
        }
    })