function readURL(input, ind) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#imagePreview' + ind).css('background-image', 'url('+e.target.result +')');
            $('#imagePreview' + ind).hide();
            $('#imagePreview' + ind).fadeIn(650);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$("#imageUpload1").change(function() {
    readURL(this, 1);
});
$("#imageUpload2").change(function() {
    readURL(this, 2);
});

// alert("hello");
