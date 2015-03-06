from django.conf.urls import patterns, include, url
from django.conf import settings

from freelance.app import views


urlpatterns = patterns('',

    url(r'^$',
        views.HomeView.as_view(),
        name='home'),

    url(r'^login$',
        views.LoginView.as_view(),
        name='login'),

    url(r'^logout$',
        views.LogoutView.as_view(),
        name='logout'),

    url(r'^invoice$',
        views.InvoiceView.as_view(),
        name='invoice_new'),

    url(r'^invoice/list$',
        views.InvoiceListView.as_view(),
        name='invoices'),

    url(r'^invoice/(?P<number>.*)$',
        views.InvoiceView.as_view(),
        name='invoice'),

    url(r'^api/invoice/(?P<pk>\d+)$',
        views.InvoiceJsonView.as_view(),
        name='api_invoice'),

    url(r'^client$',
        views.ClientView.as_view(),
        name='client_new'),

    url(r'^client/list$',
        views.ClientListView.as_view(),
        name='clients'),

    url(r'^client/(?P<pk>\d+)$',
        views.ClientView.as_view(),
        name='client'),

    url(r'^calendar$',
        views.CalendarView.as_view(),
        name='calendar'),

    url(r'^settings$',
        views.SettingsView.as_view(),
        name='settings'),

    url(r'^api/days$',
        views.DayListJsonView.as_view(),
        name='api_days'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
