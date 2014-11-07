from django.conf.urls import patterns, include, url
from django.conf import settings

from freelance.app import views


urlpatterns = patterns('',

    url(r'^login$',
        views.LoginView.as_view(),
        name='login'),

    url(r'^logout$',
        views.LogoutView.as_view(),
        name='logout'),

    url(r'^invoices/list$',
        views.InvoiceListView.as_view(),
        name='invoices'),

    url(r'^invoices/list/new$',
        views.InvoiceView.as_view(),
        name='invoice_new'),

    url(r'^invoices/list/(?P<pk>\d+)$',
        views.InvoiceView.as_view(),
        name='invoice'),

    url(r'^invoices/clients$',
        views.ClientListView.as_view(),
        name='clients'),

    url(r'^invoices/clients/new$',
        views.ClientView.as_view(),
        name='client_new'),

    url(r'^invoices/clients/(?P<pk>\d+)$',
        views.ClientView.as_view(),
        name='client'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
