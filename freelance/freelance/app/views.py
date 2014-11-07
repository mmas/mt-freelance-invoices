import json

from django.views.generic import View, ListView, TemplateView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from freelance.app.models import Invoice, Client
from freelance.app.forms import InvoiceForm, ClientForm
from freelance.app.utils import format_json


class LoginRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('login')
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class SingleObjectView(LoginRequiredMixin,
                       ModelFormMixin,
                       SingleObjectTemplateResponseMixin,
                       View):
    exclude_fields_response = ()

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        if 'pk' in kwargs:
            self.object = self.get_object()
            form = form_class(instance=self.object)
        else:
            self.object = None
            form = form_class(**self.get_form_kwargs())
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(status=201)

    def form_valid(self, form):
        obj = form.save()
        data = model_to_dict(obj, exclude=self.exclude_fields_response)
        return self._json_response(data)

    def form_invalid(self, form):
        return self._json_response(dict(form.errors), 400)

    def _json_response(self, data, status=200):
        return HttpResponse(json.dumps(data, default=format_json),
                            content_type='application/json',
                            status=status)


class MultipleObjectView(LoginRequiredMixin, ListView):
    template_name = None
    ajax_template_name = None

    def get_template_names(self):
        if self.request.is_ajax():
            template_name = self.ajax_template_name or self.template_name
        else:
            template_name = self.template_name

        if template_name is None:
            raise ImproperlyConfigured('template_name missed')

        return [template_name]


class InvoiceListView(MultipleObjectView):
    model = Invoice
    template_name = 'invoice_list.html'
    ajax_template_name = 'partials/invoice_list.html'


class InvoiceView(SingleObjectView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoice.html'
    exclude_fields_response = ('file',)


class ClientListView(MultipleObjectView):
    model = Client
    template_name = 'client_list.html'
    ajax_template_name = 'partials/client_list.html'


class ClientView(SingleObjectView):
    model = Client
    form_class = ClientForm
    template_name = 'client.html'


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


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login')
