$(document).ready(function() {
    var maxFileSize = 100000000;
    $('.avatar-preview').each(function( index ) {
        var dropZone = $(this);
        if (typeof(window.FileReader) == 'undefined') {
            dropZone.text('Не поддерживается браузером!');
            dropZone.addClass('error');
        }

        dropZone[0].ondragover = function() {
            dropZone.addClass('hover');
            return false;
        };

        dropZone[0].ondragleave = function() {
            dropZone.removeClass('hover');
            return false;
        };

        dropZone[0].ondrop = function(event) {
            event.preventDefault();
            dropZone.removeClass('hover');
            dropZone.addClass('uploaded');

            var file = event.dataTransfer.files[0];

            if (file.size > maxFileSize) {
                // dropZone.text('Файл слишком большой!');
                dropZone.addClass('error');
                return false;
            }

            var reader = new FileReader();
            reader.onload = function (e) {
                // setting preview
                setImg(e.target.result, index);
            }
            reader.readAsDataURL(file);

            // setting data
            window.images[0] = file;
        };

    });
});
