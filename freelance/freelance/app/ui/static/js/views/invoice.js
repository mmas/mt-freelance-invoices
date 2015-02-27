views.Invoice = function(data) {

    var view, template;

    console.log(data);
    view = this;

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
            }
        },
        type: 'PUT',
        url: '/api/invoice/' + data.id,
        error: function(xhr) {
            if (xhr.status == 400) error400(xhr.responseJSON);
            else error500();
        }
    });

    document.addEventListener('DOMContentLoaded', function() {
        view.element = document.getElementById('sheet');
        template = document.getElementById('template').innerHTML;
        Mustache.parse(template);
        render();
        setPopups();
        bind();
        if (!data.client) view.popups.settings.open();
    });

    function popup(id) {
        return new widgets.Popup(document.getElementById(id));
    }

    function setPopups() {
        view.popups = {
            'settings': popup('settings'),
            'delete': popup('delete-confirmation'),
            'error400': popup('error400-message'),
            'error500': popup('error500-message')
        };
    }

    function bind() {
        view.popups.settings.$element.bind('widgets.popup:accept', updateSettings);
        view.popups.delete.$element.bind('widgets.popup:accept', deleteInvoice);
    }

    function deleteInvoice() {
        $.ajax({
            type: 'DELETE'
        })
        .done(function() {
            window.location.href = '/';
        });
    }

    function updateSettings() {
        // var $form, ajax_settings;

        // $form = view.popups.settings.$element.find('form');

        // if (data.created_from == 0) {  // Invoice created from days.
        //     ajax_settings = {
        //         data: utils.serialize($form)
        //     };
        // }
        // else {  // Invoice created from file (require file).
        //     ajax_settings = {
        //         data: utils.serializeMultipart($form),
        //         cache: false,
        //         contentType: false,
        //         processData: false
        //     };
        // }
        $.ajax({
            data: utils.serialize(view.popups.settings.$element.find('form'))
        })
        .done(function(resp) {
            data = resp;
            render();
        });
    }

    function save() {
        $.ajax({
            url: '/api/invoice/' + data.id + '?save=true'
        })
        .done(function() {
            // TODO: render menu template instead.
            $('[role=menu] .inactive').removeClass('inactive');
        });
    }

    function error400(data) {
        var template;
        template = document.getElementById('error400-template').innerHTML;
        view.popups.error400.$element.find('.content').html(Mustache.render(template, data));
        view.popups.error400.open();
    }

    function error500() {
        view.popups.error500.open();
    }

    function render() {  // TODO: redefine url if data has id without refreshing.
        var content;
        if (data.pdf) content = '<img src="/media/cats.png">';  // TEMP
        if (data.created_from == 0) content = Mustache.render(template, data);
        else content = '';
        view.element.innerHTML = content;
    }

    this.save = save;

};