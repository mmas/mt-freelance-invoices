# -*- coding: utf-8 -*-

import json

from django.contrib.auth import authenticate, login, logout
# from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic

from dateutil import parser

from freelance.app.models import Invoice, Client, Day, Settings
from freelance.app.utils import serialize


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('login')
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class JsonMixin(object):

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(JsonMixin, self).dispatch(
                request, *args, **kwargs)
        except ValidationError as e:
            return HttpResponse(
                json.dumps({'errors': self._format_errors(e.message_dict)}),
                content_type='application/json',
                status=400)

    def _json_response(self, data=None, status=200, fields=[]):
        if data is not None:
            data = serialize(data, fields)
        return HttpResponse(data,
                            status=status,
                            content_type='application/json')

    def _format_errors(self, error_dict):
        return [{'field': k, 'errors': v} for k, v in error_dict.items()]


# def get_template_names(self):
#     if self.request.is_ajax():
#         template_name = self.ajax_template_name or self.template_name
#     else:
#         template_name = self.template_name

#     if template_name is None:
#         raise ImproperlyConfigured('template_name missed')

#     return [template_name]


class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home.html'


class ClientListView(LoginRequiredMixin, generic.ListView):
    model = Client
    template_name = 'client_list.html'


class ClientView(LoginRequiredMixin, generic.UpdateView):
    model = Client
    template_name = 'client.html'


class CalendarView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'calendar.html'


class JsonDayMixin(JsonMixin):
    FIELDS = ['date', 'half', 'saved']

    def _json_response(self, data=None, status=200, fields=[]):
        return super(JsonDayMixin, self)._json_response(
            data, status, self.FIELDS)


class DayListJsonView(LoginRequiredMixin, JsonDayMixin, generic.View):

    def get(self, request, *args, **kwargs):
        return self._json_response(Day.objects.get_active_days())


class DayJsonView(LoginRequiredMixin, JsonDayMixin, generic.View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        day, _ = Day.objects.get_or_create(date=data['date'])
        if not day.saved:
            day.half = data['half']
            day.save()
        return self._json_response(day)


class InvoiceMixin(object):

    def _extend_invoice(self, invoice):
        invoice_dict = model_to_dict(invoice)
        company_name = self.request.user.settings.company_name
        company_address = self.request.user.settings.company_address
        company_info = self.request.user.settings.company_info
        company_account = self.request.user.settings.company_account
        invoice_dict.update({
            'company_name': company_name,
            'company_name_html': company_name.replace('\n', '<br>'),
            'company_address': company_address,
            'company_address_html': company_address.replace('\n', '<br>'),
            'company_info': company_info,
            'company_info_html': company_info.replace('\n', '<br>'),
            'company_account': company_account,
            'days_worked_by_week': invoice.days_worked_by_week,
            'date_formatted': invoice.date_formatted,
            'daily_rate_html': invoice.daily_rate_html,
            'tax_total': invoice.tax_total,
            'subtotal_html': invoice.subtotal_html,
            'tax_total_html': invoice.tax_total_html,
            'total_html': invoice.total_html})
        tax_percent = invoice.tax * 100
        if tax_percent.is_integer():
            tax_str_format = '%d%%'
        else:
            tax_str_format = '%.2f%%'
        if invoice.client:
            invoice_dict['client'] = invoice.client
            invoice_dict['client_html'] = invoice.client.to_html()
        invoice_dict['tax_str'] = tax_str_format % tax_percent
        return invoice_dict


class InvoiceListView(LoginRequiredMixin, generic.ListView):
    model = Invoice
    template_name = 'invoice_list.html'


class InvoiceView(LoginRequiredMixin, InvoiceMixin, generic.DetailView):
    template_name = 'invoice-template.html'

    def get_object(self):
        """
        /invoice/20150103
            get invoice from number
        /invoice
            try to create an invoice from days, otherwise create empty invoice
        /invoice?from=file
            force to creat an invoice from file
        """
        if 'number' in self.kwargs:
            return self._get_object_from_number(self.kwargs['number'])

        if self.request.GET.get('from', None) == 'file':
            return self._get_new_object()

        days = Day.objects.get_active_days()
        if days:
            return self._get_object_from_days(days)

        return self._get_new_object()

    def get_context_data(self, **kwargs):
        ctx = super(InvoiceView, self).get_context_data(**kwargs)
        ctx['object_json'] = serialize(self._extend_invoice(self.object))
        ctx['clients'] = Client.objects.all()
        return ctx

    def _get_object_from_number(self, number):
        return Invoice.objects.get(number=number)

    def _get_object_from_days(self, days):
        """Get a new invoice created from active days."""
        invoice = Invoice.objects.create(
            daily_rate=self.request.user.settings.default_daily_rate,
            tax=self.request.user.settings.default_tax)
        for i in days:
            i.invoice = invoice
            i.save()
        invoice.save()  # Set subtotal from days.
        return invoice

    def _get_new_object(self):
        return Invoice.objects.create(
            daily_rate=self.request.user.settings.default_daily_rate,
            tax=self.request.user.settings.default_tax,
            created_from=1)


class InvoiceJsonView(
        JsonMixin, LoginRequiredMixin, InvoiceMixin, generic.View):

    def put(self, request, *args, **kwargs):
        invoice = self.get_object()
        if 'save' in request.GET:
            invoice.status = 1
            invoice.full_clean()  # Validate blank fields, not the best way.
            invoice.save()
            return self._json_response(status=201)
        else:
            for k, v in json.loads(request.body).items():
                if k == 'client':
                    v = Client.objects.get(pk=v)
                elif k == 'date':
                    # Convert before saving to keep date as a DateTime object.
                    v = parser.parse(v)
                setattr(invoice, k, v)
            invoice.save()
            return self._json_response(self._extend_invoice(invoice))

    def delete(self, request, *args, **kwargs):
        invoice = self.get_object()
        invoice.delete()
        return self._json_response(status=201)

    def get_object(self):
        return Invoice.objects.get(pk=self.kwargs['pk'])


class SettingsView(LoginRequiredMixin, generic.UpdateView):
    model = Settings
    template_name = 'settings.html'

    def get_object(self, queryset=None):
        return self.request.user.settings

    def get_success_url(self):
        return reverse('settings')


class LoginView(generic.TemplateView):
    template_name = 'login.html'

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('invoices')
        return redirect('login')


class LogoutView(LoginRequiredMixin, generic.View):

    def get(self, request):
        logout(request)
        return redirect('login')
