from django.forms import widgets
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.translation import ugettext as _


# Don't load javascript as Media.js since this won't work if async.


class BootstrapInputMixin(object):

    def render(self, name, value, attrs={}):
        attrs['class'] = 'form-control'
        return super(BootstrapInputMixin, self).render(name, value, attrs)


class TextInput(BootstrapInputMixin, widgets.TextInput):
    pass


class EmailInput(BootstrapInputMixin, widgets.EmailInput):
    pass


class Textarea(BootstrapInputMixin, widgets.Textarea):
    pass


class Select(BootstrapInputMixin, widgets.Select):
    pass


class NumberInput(BootstrapInputMixin, widgets.NumberInput):
    pass


class DateInput(BootstrapInputMixin, widgets.TextInput):

    def render(self, name, value, attrs={}):
        attrs['placeholder'] = 'yyyy/mm/dd'
        return super(DateInput, self).render(name, value, attrs)

    def _format_value(self, value):
        return value.strftime('%Y/%m/%d')


class FileInput(widgets.FileInput):

    def render(self, name, value, attrs={}):
        button = ('<button class="btn btn-default btn-block" '
                  'onclick="triggerFileInput(event)">'
                  '%s</button>')
        if value and hasattr(value, 'url'):
            button = button % _('Change')
        else:
            button = button % _('Upload')
        attrs['class'] = 'hidden'
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        return format_html('%s<input%s />' % (button, flatatt(final_attrs)))
