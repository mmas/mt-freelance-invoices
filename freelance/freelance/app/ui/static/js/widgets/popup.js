widgets.Popup = function(element) {

    var self, box;

    self = this;
    self.element = element;
    self.$element = $(element);
    box = self.element.parentElement;

    self.$element.find('[data-close]').bind('click', close);
    self.$element.find('[data-accept]').bind('click', accept);

    function close() {
        box.style.display = 'none';
        self.element.style.display = 'none';
        self.$element.trigger('widgets.popup:close');
    };

    function accept() {
        self.$element.trigger('widgets.popup:accept');
        self.close();
    };

    function open() {
        box.style.display = 'block';
        self.element.style.display = 'block';
        self.$element.trigger('widgets.popup:open');
    }

    this.close = close;
    this.accept = accept;
    this.open = open;

};