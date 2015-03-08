views.Client = function() {

    view = this;

    document.addEventListener('DOMContentLoaded', function() {
        view.popups = {
            delete: utils.popup('delete-confirmation')
        };
    });

};