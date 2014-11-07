(function() {

    triggerFileInput = function(e) {
        e.preventDefault();
        $(e.target).siblings('[type=file]').click();
    }

})();