$(document).ready(function(){
    // Назначим обработчик события на кнопку
    $("#button-order1").on('click', function(){
        const type_order1 = $('#type_order1').val();
        const address1 = $('#address1').val();
        $('#type_order').val(type_order1);
        $('#address').val(address1);
    });
});
$(document).ready(function(){
    // Назначим обработчик события на кнопку
    $("#button-order2").on('click', function(){
        const type_order2 = $('#type_order2').val();
        const address2 = $('#address2').val();
        $('#type_order').val(type_order2);
        $('#address').val(address2);
    });
});
