$(function(){
    $('#landing-img').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
        $("#div-header").addClass("animated fadeInDown");
        $("#show-login").addClass("animated fadeInDown");
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (settings.type === 'POST' || settings.type === 'PUT' || settings.type === 'DELETE') {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie !== '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs i.e. locally.
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        }
    });

});

function show_login(){
    $('#landing-div').addClass('animated slideOutUp');
    $('#landing-div').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
        $("#login-form").fadeIn();
        open_camera();
    });
}

function open_camera(){
    Webcam.set({
        width: 500,
        height: 450,
        dest_width: 640,
        dest_height: 480,
        image_format: 'jpeg',
        jpeg_quality: 90,
        force_flash: false
    });
    Webcam.attach('#camera');
}

function take_snapshot(){

    Webcam.snap(function(data_uri){
        Webcam.freeze();
        var raw_data = data_uri.replace(/^data\:image\/\w+\;base64\,/,"");
        $.ajax({
            url: '',
            method: 'POST',
            data: {
                csrfmiddlewaretoken: getCsrfCookie(),
                raw_data: raw_data
            },
            beforeSend: function(){
                $("#loader").fadeIn();
            },
            success: function(user_id){
                $("#loader").fadeOut();
                window.location = '/home_dashboard/' + user_id;
            },
            error: function(xhr){
                $("#loader").fadeOut();
                if (xhr.responseText==="redirect"){
                    window.location = '/registration_page/';
                }else if(xhr.responseText==="not_recognized"){
                    $("#msg-body").html("Unable to recognize you. Try Again!");
                    $("#msg-header").html("Unable to recognize");
                    $("#msg-modal").modal("show");
                }
            }
        });
    });

}

function getCsrfCookie() {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, 'csrftoken'.length + 1) === ('csrftoken=')) {
                cookieValue = decodeURIComponent(cookie.substring('csrftoken'.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}