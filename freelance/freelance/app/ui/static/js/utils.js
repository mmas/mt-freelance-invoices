utils = {};

utils.serialize = function(form, to_json) {  // TODO: encode files.
    var data, $form, i, xi, number_fields;
    to_json = to_json === undefined ? true : to_json;
    data = {};
    $form = $(form);
    form = $form.serializeArray();
    number_fields = [];
    $form.find('[name]').filter('[type=number]').each(function() { number_fields.push(this.name); })
    for (i=0; xi=form[i]; i++) {
        if (number_fields.indexOf(xi.name) == -1) data[xi.name] = xi.value;
        else data[xi.name] = parseFloat(xi.value);
    }
    if (to_json) data = JSON.stringify(data);
    return data;
}


utils.serializeMultipart = function(form) {
    var form_data, fields, file_fields, file, field, i, j;
    fields = utils.serialize(form, false);
    file_fields = $(form).find('[type=file],[type=image]');
    form_data = new FormData();
    console.log('files');
    for (i=0; field=file_fields[i]; i++) {
        for (j=0; file=field.files[j]; j++) {
            console.log(field.name, file);
            form_data.append(field.name, file);
        }
    }
    console.log('fields');
    for (field in fields) {
        console.log(field, fields[field]);
        form_data.append(field, fields[field]);
    }
    return form_data;
}
