(function() {

    var $object_list, $object_new, $object_edit,
        $msg_object_created, $msg_object_updated, $msg_object_deleted, $msg_error;

    $object_list = $('#object-list');
    $object_new = $('#object-new');
    $object_new_body = $object_new.find('.modal-body');
    $object_edit = $('#object-edit');
    $object_edit_body = $object_edit.find('.modal-body');
    $msg_object_created = $('#msg-object-created');
    $msg_object_updated = $('#msg-object-updated');
    $msg_object_deleted = $('#msg-object-deleted');
    $msg_error = $('#msg-error');

    $object_new.on('shown.bs.modal', function(){
        if (! $object_new_body.find('form').length) {
            $.get(NEW_URL, function(resp) { $object_new_body.html(resp); });
        }
    });

    $object_new.on('hidden.bs.modal', function(){
        $object_new_body.find('form')[0].reset();
        $object_new_body.find('.has-error').removeClass('has-error');
    });

    $object_edit.on('shown.bs.modal', function(e){
        $.get(EDIT_URL, function(resp) {
            $(e.target).find('.modal-body').html(resp);
        });
    });

    $object_edit.on('hidden.bs.modal', function(){
        // $object_edit_body.find('form')[0].reset();  // This is not working.
        $object_edit_body.empty();
    });

    showEditObject = function(url) {
        EDIT_URL = url;
        $object_edit.modal('show');
    }

    createObject = function(e) {
        var $form;

        e.preventDefault();

        $form = $(e.target);
        $form.find('.has-error').removeClass('has-error');

        $.ajax({
            type: 'POST',
            url: NEW_URL,
            data: getFormData($form),
            cache: false,
            contentType: false,
            processData: false
        })
        .done(function(data, status, error) {
            $object_new.modal('hide');
            showMessage($msg_object_created);
            listObjects();
        })
        .fail(function(xhr, status, error) {
            for (var i in xhr.responseJSON) {
                $form.find('[name='+i+']').closest('.form-group').addClass('has-error');
            }
        });
    }

    updateObject = function(e) {
        var $form;

        e.preventDefault();

        $form = $(e.target);
        $form.find('.has-error').removeClass('has-error');

        $.ajax({
            type: 'POST',  // Use POST instead of PUT since data is a form, not json.
            url: EDIT_URL,
            data: getFormData($form),
            cache: false,
            contentType: false,
            processData: false
        })
        .done(function(data, status, error) {
            $object_edit.modal('hide');
            showMessage($msg_object_updated);
            listObjects();
        })
        .fail(function(xhr, status, error) {
            for (var i in xhr.responseJSON) {
                $form.find('[name='+i+']').closest('.form-group').addClass('has-error');
            }
        });
    }

    deleteObject = function(e) {
        var csrftoken;

        e.preventDefault();

        csrftoken = $(e.target).closest('.modal').find('[name=csrfmiddlewaretoken]').val();
        $.ajax({
            type: 'DELETE',
            beforeSend: function(xhr) { xhr.setRequestHeader('X-CSRFToken', csrftoken); },
            url: EDIT_URL
        })
        .done(function(data, status, error) {
            $object_edit.modal('hide');
            showMessage($msg_object_deleted);
            listObjects();
        })
        .fail(function(xhr, status, error) {
            $object_edit.modal('hide');
            showMessage($msg_error);
        });
    }

    listObjects = function() {
        $object_list.addClass('loading');
        $.get(LIST_URL, function(data) {
            $object_list.html(data);
            $object_list.removeClass('loading');
        });
    }

    submitForm = function(el) {
        $(el).closest('.modal').find('form').submit()
    }

    showMessage = function($msg) {
        $msg.removeClass('hidden');
        $msg.addClass('active');
        setTimeout(function() {
            $msg.removeClass('active');
            setTimeout(function() {
                $msg.removeClass('hidden');
            }, 1000);
        }, 4000);
    }

    getFormData = function($form) {
        var data;
        data = new FormData();
        $form.find('[name]').each(function(i, el) {
            data.append(el.name, (el.files && el.files.length) ? el.files[0] : el.value);
        });
        return data;
    }

    openFile = function(e) {
        var url;
        e.preventDefault();
        url = $(e.target).closest('.modal').find('[data-file]').attr('data-file');
        if (url) window.open(url, '_newtab');
    }

})();