function processPhoto() {
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
    request.open("POST", '/app/photoupload');
    request.send(formData);
}

function okCallback(data) {
    alert(data);
}
