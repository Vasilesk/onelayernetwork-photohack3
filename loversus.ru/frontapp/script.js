function processPhoto() {
    if (window.images[0] == null) {
        $('.avatar-preview').addClass('error');
        return;
    }

    let photo = window.images[0];  // file from input
    // console.log(photo);

    let request = new XMLHttpRequest();
    request.onreadystatechange = function() {
       if (request.readyState == 4 && request.status == 200)
       {
           okCallback(request.responseText); // Another callback here
       }
    };
    let formData = new FormData();

    formData.append("photo", photo);
    formData.append("hunter_id", window.hunterId);
    request.open("POST", '/app/photoupload');
    request.send(formData);

    window.setTimeout(function() {
        $('#winmodal').iziModal('open');
    }, 1000);
}

function getHunterId() {
    var url = document.createElement('a');
    url.href = window.location.href;

    if (url.pathname.length == 1) {
        return "0";
    }
    // return parseInt(url.pathname.substring(1));
    return url.pathname.substring(1);
}

function okCallback(dataStr) {
    var data = JSON.parse(dataStr);
    console.log(data);
    if (data.status == "ok") {
        $("#img-modal").attr("src", data.url);
        // $("#img-modal").attr("src", "https://loversus.ru/processed/"+data.hunterized+".png");
    }
}

function fetchCounter() {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function() {
       if (request.readyState == 4 && request.status == 200)
       {
           var data = JSON.parse(request.responseText);
           if (data.status == "ok") {
               $("#bitecounter").text(data.count);
           }
       }
    };
    let formData = new FormData();

    formData.append("hunter_id", window.hunterId);
    request.open("POST", '/app/bitecount');
    request.send(formData);
}

$(document).ready(function() {
    window.hunterId = getHunterId();
    fetchCounter();

    $("#img-hunter").attr("src", "https://loversus.ru/processed/"+window.hunterId+".png")
});
