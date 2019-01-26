function setPreview(data, ind) {
    var elem = $('#imagePreview' + ind);
    elem.css('background-image', 'url('+ data +')');
    elem.hide();
    elem.fadeIn(650);
}

function readURL(input, ind) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            setPreview(e.target.result, ind);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function onUpload(ind) {
    readURL(this, ind + 1);
    $($('.avatar-preview')[ind]).addClass('uploaded');
}

$("#imageUpload1").change(function() {
    onUpload(0);
});
$("#imageUpload2").change(function() {
    onUpload(1);
});

// alert("hello");
