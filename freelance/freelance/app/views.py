import json

from django.core.urlresolvers import reverse
from django.views.generic import View, ListView, TemplateView, UpdateView
from django.http import HttpResponse
# from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from freelance.app.models import Invoice, Client, Day, Settings
# from freelance.app.forms import InvoiceForm, ClientForm
from freelance.app.utils import format_json


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('login')
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


# def get_template_names(self):
#     if self.request.is_ajax():
#         template_name = self.ajax_template_name or self.template_name
#     else:
#         template_name = self.template_name

#     if template_name is None:
#         raise ImproperlyConfigured('template_name missed')

#     return [template_name]


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'invoice_list.html'


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client_list.html'


class InvoiceView(LoginRequiredMixin, UpdateView):
    model = Invoice
    # form_class = InvoiceForm
    template_name = 'invoice.html'
    exclude_fields_response = ('file',)

    def get_object(self, queryset=None):
        return self.model.objects.get(number=self.kwargs['number'])


class ClientView(LoginRequiredMixin, UpdateView):
    model = Client
    # form_class = ClientForm
    template_name = 'client.html'


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'calendar.html'


class DayListJsonView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        days = Day.objects.all()
        return HttpResponse(json.dumps(list(days.values('date', 'status')),
                                       default=format_json),
                            content_type='application/json')


class DayJsonView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        day, _ = Day.objects.get_or_create(date=data['date'])
        day.status = data['status']
        day.save()
        return HttpResponse(status=201)


class SettingsView(LoginRequiredMixin, UpdateView):
    model = Settings
    template_name = 'settings.html'

    def get_object(self, queryset=None):
        return self.request.user.settings

    def get_success_url(self):
        return reverse('settings')


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('invoices')
        return redirect('login')


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('login')
