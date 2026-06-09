/* =========================
   GOOGLE PLACES AUTOCOMPLET
========================= */

/* =========================
   HANDLE BROWSER BACK CACHE
========================= */
window.addEventListener('pageshow', function (event) {
    if (event.persisted) {
        window.location.reload();
    }
});


let autocomplete;

function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: { country: ['in'] }
        }
    );
    autocomplete.addListener("place_changed", onPlaceChanged);
}

function onPlaceChanged() {
    const place = autocomplete.getPlace();
    console.log('Place selected:', place);

    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
        return;
    }

    const latitude = place.geometry.location.lat();
    const longitude = place.geometry.location.lng();

    $('#id_latitude').val(latitude.toFixed(6));
    $('#id_longitude').val(longitude.toFixed(6));

    if (place.name) {
        $('#id_address').val(place.name);
    }

    place.address_components.forEach(component => {
        component.types.forEach(type => {
            if (type === 'country') $('#id_country').val(component.long_name);
            if (type === 'administrative_area_level_1') $('#id_state').val(component.long_name);
            if (type === 'locality') $('#id_city').val(component.long_name);
            if (type === 'postal_code') $('#id_pin_code').val(component.long_name);
        });
    });
}


/* =========================
   DOCUMENT READY
========================= */

$(document).ready(function () {

    /* ========= ADD TO CART ========= */
    $(document).on('click', '.add_to_cart', function (e) {
        e.preventDefault();

        let food_id = $(this).data('id');
        let url = $(this).data('url');

        $.ajax({
            type: 'GET',
            url: url,
            data: { food_id: food_id },
            headers: { "X-Requested-With": "XMLHttpRequest" },
            success: function (response) {
                if(response.status == 'login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)

                    // Simplified Feedback: Change text to 'Added to Cart'
                    let addBtn = $('#add-btn-' + food_id);
                    if (addBtn.length > 0) {
                        addBtn.addClass('blinkit-added').text('Added to Cart');
                    }

                    applyamount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    )
                }
            }
        });
    });

    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)
    })


    /* ========= DECREASE CART ========= */
    $(document).on('click', '.decrease_cart', function (e) {
        e.preventDefault();

        let food_id = $(this).data('id');
        let cart_id = $(this).data('cart-id');
        let url = $(this).data('url');

        $.ajax({
            type: 'GET',
            url: url,
            data: { food_id: food_id },
            headers: { "X-Requested-With": "XMLHttpRequest" },
            success: function (response) {
                if(response.status == 'login_required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                } else if (response.status === 'failed') {
                    Swal.fire({ icon: 'error', title: response.message });
                } else {
                    $('#cart_counter').html(response.cart_counter.cart_count);
                    $('#qty-' + food_id).html(response.qty);

                    // Note: Selector toggle removed per simplicity request
                    applyamount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    )


                    if (parseInt(response.qty) <= 0) {
                        $('#cart-item-' + cart_id).fadeOut(300, function () {
                            $(this).remove();
                            displayEmptyText();
                        });
                    }
                }
            }
        });
    });


    /* ========= DELETE CART ITEM ========= */
    $(document).on('click', '.delete_item', function (e) {
        e.preventDefault();

        let food_id = $(this).data('id');
        let url = $(this).data('url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status === 'failed') {
                    Swal.fire({ icon: 'error', title: response.message });
                } else {
                    $('#cart_counter').html(response.cart_counter.cart_count);
                    applyamount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    )
                    $('#cart-item-' + food_id).fadeOut(300, function () {
                        $(this).remove();
                        displayEmptyText();
                    });
                    Swal.fire('Success', response.message, 'success');
                }
            }
        });
    });


    /* ========= ADD OPENING HOURS ========= */
    $(document).on('click', '.add_hour', function (e) {
        e.preventDefault();

        let day = $('#id_day').val();
        let from_hour = $('#id_from_hour').val();
        let to_hour = $('#id_to_hour').val();
        let is_closed = $('#id_is_closed').is(':checked');
        let csrf_token = $('input[name=csrfmiddlewaretoken]').val();
        let url = $(this).data('url');

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                day: day,
                from_hour: from_hour,
                to_hour: to_hour,
                is_closed: is_closed,
                csrfmiddlewaretoken: csrf_token
            },
            success: function (response) {

                if (response.status === 'success') {
                    let html = response.is_closed
                        ? `<tr><td><b>${response.day}</b></td><td>Closed</td><td><a href="#">Remove</a></td></tr>`
                        : `<tr><td><b>${response.day}</b></td><td>${response.from_hour} - ${response.to_hour}</td><td><a href="#">Remove</a></td></tr>`;

                    $('.opening_hours').append(html);
                    $('#opening_hours')[0].reset();

                    Swal.fire({
                        title: 'Added successfully!',
                        icon: 'success',
                        timer: 1000,
                        showConfirmButton: false
                    });
                } else {
                    Swal.fire(response.message, '', 'error');
                }
            }
        });
    });


    /* ========= REMOVE OPENING HOURS ========= */
    $(document).on('click', '.remove_hour', function (e) {
        e.preventDefault();

        let url = $(this).data('url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status === 'success') {
                    $('#hour-' + response.id).fadeOut(300, function () {
                        $(this).remove();
                    });

                    Swal.fire({
                        title: 'Deleted!',
                        text: 'Opening hour removed successfully.',
                        icon: 'success',
                        timer: 1000,
                        showConfirmButton: false
                    });
                }
            }
        });
    });

});


/* =========================
   HELPER FUNCTIONS
========================= */

function displayEmptyText() {
    let cart_counter = parseInt($('#cart_counter').html());
    if (cart_counter === 0) {
        $('#check-cart').show();
    }
}






function applyamount(subtotal, tax, grand_total) {
    if (window.location.pathname === '/cart/') {
        $('#subtotal').html(subtotal);
        $('#total').html(grand_total);

        // update each tax dynamically
        for (const [tax_type, tax_data] of Object.entries(tax)) {
            for (const [percentage, amount] of Object.entries(tax_data)) {
                $('#tax-' + tax_type).html(amount);
            }
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const alertBox = document.querySelector(".show-notification");

    if (alertBox) {
        setTimeout(() => {
            alertBox.classList.add("fade-out");

            setTimeout(() => {
                alertBox.remove();
            }, 500); // match CSS transition
        }, 3000); // visible time
    }
});

