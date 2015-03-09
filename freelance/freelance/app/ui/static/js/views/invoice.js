views.Invoice = function(data) {

    console.log(data);

    var view, templates, menu, info;

    view = this;
    view.update = update;
    view.email = email;

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'));
            }
        },
        type: 'PUT',
        url: '/api/invoice/' + data.id,
        error: function(xhr) {
            view.popups.loading.close();
            if (xhr.status == 400) error400(xhr.responseJSON);
            else error500();
        }
    });

    document.addEventListener('DOMContentLoaded', function() {
        var $file;

        view.element = document.getElementById('sheet');
        menu = document.getElementById('menu');
        info = document.getElementById('info-content');
        templates = {
            main: document.getElementById('template').innerHTML,
            menu: document.getElementById('menu-template').innerHTML,
            info: document.getElementById('info-template').innerHTML
        };
        Mustache.parse(templates.main);
        render();
        renderMenu();
        renderInfo();
        view.popups = {
            'loading': utils.popup('loading'),
            'settings': utils.popup('settings', {'accept': function() { update(); }}),
            'info': utils.popup('info'),
            'delete': utils.popup('delete-confirmation'),
            'error400': utils.popup('error400-message'),
            'error500': utils.popup('error500-message'),
            'save': utils.popup('save-confirmation', {'accept': function() { update('save'); }}),
            'sent': utils.popup('sent-confirmation'),
            'password': utils.popup('email-password', {'accept': onAcceptPassword}),
            'upload': utils.popup('upload-file', {'accept': onAcceptUpload}),
        };
        if (data.created_from == 0) {  // From calendar.
            if (!data.client) view.popups.settings.open();
        }
        else {  // From file.
            if (!data.pdf) view.popups.upload.open();
            else if (!data.client) view.popups.settings.open();
        }
    });

    function onAcceptPassword(e) {
        email($(e.target).find('input[type="password"]').val());
    }

    function onAcceptUpload(e) {
        var pdf;
        pdf = $(e.target).find('[name="pdf"]')[0];
        if (pdf.files.length) update('file', pdf.files[0]);
    }

    function clean() {
        data.company_address = data.company_address.replace(/\n/g, '<br>');
        data.company_info = data.company_info.replace(/\n/g, '<br>');
        if (data.client) {
            data.client.address = data.client.address.replace(/\n/g, '<br>');
        }
    }

    function update(mode, file) {
        var form_data;

        if (mode == 'save') {
            $.ajax({
                url: '/api/invoice/' + data.id + '?save=true'
            })
            .done(function(resp) {
                data = resp;
                renderMenu();
                renderInfo();
            });
        }
        else if (mode == 'paid') {
            $.ajax({
                data: JSON.stringify({date_paid: utils.isodate(new Date())})
            })
            .done(function(resp) {
                data = resp;
                renderMenu();
                renderInfo();
            });
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
                renderInfo();
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
                renderInfo();
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

    function email(password) {
        view.popups.loading.open();
        $.ajax({
            url: '/api/invoice/' + data.id + '?email=true',
            data: JSON.stringify({password: password})
        })
        .done(function(resp) {
            view.popups.loading.close();
            view.popups.sent.open();
            data = resp;
            renderMenu();
            renderInfo();
        });
    }

    function render() {
        var content;
        clean(data);
        if (data.created_from == 0) {
            content = Mustache.render(templates.main, data);
        }
        else if (data.pdf) {
            content = '<object type="application/pdf" data="' + data.pdf + '"></object>';
        }
        else {
            content = '';
        }
        view.element.innerHTML = content;
    }

    function renderMenu() {
        menu.innerHTML = Mustache.render(templates.menu, data);
    }

    function renderInfo() {
        info.innerHTML = Mustache.render(templates.info, data);
    }

};