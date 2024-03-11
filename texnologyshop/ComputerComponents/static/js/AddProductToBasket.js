$(document).ready(function(){
    // Назначим обработчик события на кнопку
    $(".button-add-product").on('click', function(){
        const product_id = $(this).data('product_id');
        AddProductToBasketAJAX(product_id);
    });
});
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
                }
            }
        }
    return cookieValue;
}
function AddProductToBasketAJAX(product_id){
    $.ajax({
        url: '/baskets/add_product/',
        type: 'POST',
        data: {
            'product_id': product_id
        },
        dataType: 'json',
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        },
        success: function(data){
            if (data.message) {
                $('.push-sms').css("display", "block");
                setTimeout(function()
            {
                $('.push-sms').css("display", "none");
            }, 5000);
            }
        },
        error: function(data){
            console.log('Ошибка:', data.error);
        }
    });
}
