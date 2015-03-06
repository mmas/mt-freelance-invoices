views.Invoice = function(data) {

    console.log(data);

    var view, template;

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
        var $file;

        view.element = document.getElementById('sheet');
        template = document.getElementById('template').innerHTML;
        Mustache.parse(template);
        render();
        view.popups = {
            'settings': utils.popup('settings', {'widgets.popup:accept': function() { update(); }}),
            'info': utils.popup('info'),
            'delete': utils.popup('delete-confirmation'),
            'error400': utils.popup('error400-message'),
            'error500': utils.popup('error500-message'),
            'save': utils.popup('save-confirmation', {'widgets.popup:accept': function() { update('save'); }})
        };
        if (data.created_from == 0) {  // From calendar.
            if (!data.client) {
                view.popups.settings.open();
            }
        }
        else {  // From file.
            if (!data.pdf) {
                $file = $('[name="pdf"]')
                $file.click();
                $file.bind('change', function(e) {
                    if (e.target.files.length) update('file', e.target.files[0]);
                });
            }
            else if (!data.client) {
                view.popups.settings.open();
            }
        }
    });

    function clean() {
        data.company_address = data.company_address.replace(/\n/g, '<br>');
        data.company_info = data.company_info.replace(/\n/g, '<br>');
    }

    function update(mode, file) {
        var form_data;

        if (mode == 'save') {
            $.ajax({
                url: '/api/invoice/' + data.id + '?save=true'
            })
            .done(function() {
                // TODO: render menu template.
            });
        }
        else if (mode == 'paid') {
            $.ajax({
                data: JSON.stringify({date_paid: new Date().toJSON().split('T')[0]})
            });
            // TODO: render menu template in done().
        }
        else if (mode == 'file') {
            form_data = new FormData();
            form_data.append('pdf', file);
            $.ajax({
                data: form_data,
                type: 'POST',
                cache: false,
                contentType: false,
                processData: false
            })
            .done(function(resp) {
                data = resp;
                render();
                if (!data.client) view.popups.settings.open();
            });
        }
        else {
            $.ajax({
                data: utils.serialize(view.popups.settings.$element.find('form'))
            })
            .done(function(resp) {
                data = resp;
                render();
            });
        }
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

    function render() {
        var content;
        clean(data);
        if (data.created_from == 0) {
            content = Mustache.render(template, data);
        }
        else if (data.pdf) {
            content = '<object type="application/pdf" data="' + data.pdf + '"></object>';
        }
        else {
            content = '';
        }
        view.element.innerHTML = content;
    }

    this.update = update;

};