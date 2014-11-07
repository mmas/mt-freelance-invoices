from django import forms
from django.utils.translation import ugettext as _

from dateutil.parser import parse as parse_datetime

from freelance.app.models import Invoice, Client
from freelance.app.ui import widgets


STATUS_CHOICES = (('draft', _('Draft')),
                  ('sent', _('Sent')),
                  ('paid', _('Paid')))


class InvoiceForm(forms.ModelForm):

    def __init__(self, data=None, *args, **kwargs):
        # Parse date before clean. TODO: find better way.
        if data:
            for i in ['date', 'date_paid']:
                date = data.get(i)
                if date:
                    data[i] = parse_datetime(date)
        super(InvoiceForm, self).__init__(data, *args, **kwargs)

    class Meta:
        model = Invoice
        exclude = ('created', 'updated', 'total',)
        widgets = {'number': widgets.TextInput,
                   'date': widgets.DateInput,
                   'date_paid': widgets.DateInput,
                   'client': widgets.Select,
                   'subtotal': widgets.NumberInput,
                   'tax': widgets.NumberInput,
                   'file': widgets.FileInput,
                   'status': widgets.Select(choices=STATUS_CHOICES)}


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        widgets = {'name': widgets.TextInput,
                   'address': widgets.Textarea(attrs={'rows': '3'}),
                   'email': widgets.EmailInput}
