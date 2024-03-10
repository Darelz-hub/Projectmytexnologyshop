$(document).ready(function(){
    // Назначим обработчик события на кнопку
    $("#AddProductToBasket").on('click', function(){
        const product_id = $(this).data('product');
        AddProductToBasketAJAX(product_id);
    });
});
function AddProductToBasketAJAX(product_id){
    $.ajax({
        url: 'baskets/add_product/',
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
                alert(data.message);
            }
        },
        error: function(error){
            console.log('Ошибка:', error);
        }
    });
}
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