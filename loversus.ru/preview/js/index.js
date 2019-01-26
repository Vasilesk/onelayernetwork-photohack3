function setImg(data, ind) {
    var elem = $('#imagePreview' + (ind + 1));
    elem.css('background-image', 'url('+ data +')');
    elem.hide();
    elem.fadeIn(650);
}

function readURL(input, ind) {
    if (input.files && input.files[0]) {
        window.images[ind] = input.files[0];
        var reader = new FileReader();
        reader.onload = function(e) {
            setImg(e.target.result, ind);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function onUpload(ind, input) {
    readURL(input, ind);
    $($('.avatar-preview')[ind]).addClass('uploaded');
}

// setting preview and data
$("#imageUpload1").change(function() {
    onUpload(0, this);
});
$("#imageUpload2").change(function() {
    onUpload(1, this);
});

$(".avatar-preview").each(function (ind) {
    var elem = $(this);
    elem.click(function() {
        $("#imageUpload" + (ind + 1)).click();
    });
});

$(document).ready(function () {
    window.images = [null, null];
});
