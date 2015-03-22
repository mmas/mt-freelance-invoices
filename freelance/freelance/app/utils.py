# -*- coding: utf-8 -*-

import json
from datetime import datetime, date

from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.db.models import Model, QuerySet
from django.db.models.fields.files import FieldFile
from django.forms.models import model_to_dict


def json_default_encode(x):
    """Allow date and datetime JSON encoding."""
    if isinstance(x, (datetime, date)):
        return x.isoformat()
    elif isinstance(x, Model):
        return x.pk
    elif isinstance(x, FieldFile) and hasattr(x, 'file'):
        return x.url


def serialize(x, fields=[], as_json=True, recursive=True):
    """JSON serialize from a model or a queryset."""
    if isinstance(x, QuerySet):  # TODO: recurive as well.
        y = list(x.values(*fields))
    elif isinstance(x, Model):
        y = model_to_dict(x)
        if fields:
            y = dict((i, y[i]) for i in fields)
        if recursive:
            for i in y.keys():
                attr = getattr(x, i)
                if isinstance(attr, Model):
                    y[i] = serialize(attr, as_json=False)
    elif isinstance(x, (list, tuple)) and fields:
        y = [dict((i, j[i]) for i in fields) for j in x]  # TODO: ..and here.
    elif isinstance(x, dict):
        if fields:
            y = dict((i, x[i]) for i in fields)
        else:
            y = x
        if recursive:
            for k, v in y.items():
                if isinstance(v, Model):
                    y[k] = serialize(v, as_json=False)
    else:
        y = x
    if as_json:
        y = json.dumps(y, default=json_default_encode)
    return y


def serialize_invoice(invoice, usettings, as_json=True):
    data = serialize(invoice, as_json=False)
    data.update({
        'company_name': usettings.company_name,
        'company_address': usettings.company_address,
        'company_info': usettings.company_info,
        'company_account': usettings.company_account,
        'days_worked_by_week': invoice.days_worked_by_week(usettings),
        'date__str': usettings.format_date(invoice.date),
        'daily_rate__str': usettings.format_money(invoice.daily_rate),
        'tax_total': invoice.tax_total,
        'subtotal__str': usettings.format_money(invoice.subtotal),
        'tax_total__str': usettings.format_money(invoice.tax_total),
        'total__str': usettings.format_money(invoice.total),
        'saved': invoice.saved,
        'sent': invoice.sent,
        'paid': invoice.paid,
        'created__str': invoice.created.strftime('%Y-%m-%d %H:%M'),
        'updated__str': invoice.updated.strftime('%Y-%m-%d %H:%M')})
    tax_percent = invoice.tax * 100
    tax_str_format = '%d%%' if tax_percent.is_integer() else '%.2f%%'
    if invoice.date_paid:
        data['date_paid__str'] = usettings.format_date(invoice.date_paid),
    data['tax__str'] = tax_str_format % tax_percent
    return serialize(data, as_json=as_json)


def email_invoice(invoice, usettings, password):
    backend = EmailBackend(host=usettings.email_smtp,
                           port=usettings.email_smtp_port,
                           username=usettings.email_address,
                           password=password,
                           use_tls=(usettings.email_protocol == 0),
                           use_ssl=(usettings.email_protocol == 1))
    email = EmailMessage(invoice.number, '', usettings.email_address,
                         [invoice.client.email], connection=backend)
    email.attach_file(invoice.pdf.path)
    email.send()
