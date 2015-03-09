utils = {};

utils.popup = function(id, events) {
    var popup, i;
    popup = new widgets.Popup(document.getElementById(id));
    if (events) for (i in events) popup.$element.bind('widgets.popup:'+i, events[i]);
    return popup;
}

utils.serialize = function(form, to_json) {
    var data, data_, $form, i, xi, ready, wait, $files, fname, reader;

    $form = $(form);
    data_ = $form.serializeArray();
    data = {}; for (i=0; xi=data_[i]; i++) data[xi.name] = xi.value;

    // Filter numeric fields to serialize them as numbers.
    $form.find('[name]').filter('[type=number]').each(function() {
        data[this.name] = parseFloat(this.value);
    });

    if (to_json === undefined ? true : to_json) data = JSON.stringify(data);
    return data;
}

utils.base64 = function(file, callback) {
    var reader;
    reader = new FileReader();
    reader.onloadend = function(e) {
        callback(e.target.result);
    };
    reader.readAsDataURL(file);
}

utils.isodate = function(x) {
    return x.toJSON().split('T')[0];
};
