widgets.Popup = function(element) {
    var widget, box;

    widget = this;
    widget.element = element;
    widget.$element = $(element);
    box = widget.element.parentElement;

    widget.close = function() {
        box.style.display = 'none';
        widget.element.style.display = 'none';
        widget.$element.trigger('widgets.popup:close');
    };

    widget.accept = function() {
        widget.close();
        widget.$element.trigger('widgets.popup:accept');
    };

    widget.open = function() {
        box.style.display = 'block';
        widget.element.style.display = 'block';
        widget.$element.trigger('widgets.popup:open');
    }

    widget.$element.find('[data-close]').bind('click', widget.close);
    widget.$element.find('[data-accept]').bind('click', widget.accept);
};