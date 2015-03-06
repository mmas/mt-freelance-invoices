# -*- coding: utf-8 -*-

import json
from datetime import datetime, date

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


def serialize(x, fields=[], as_json=True):
    """JSON serialize from a model or a queryset."""
    if isinstance(x, QuerySet):
        x = list(x.values(*fields))
    elif isinstance(x, Model):
        x = model_to_dict(x)
        if fields:
            x = dict((i, x[i]) for i in fields)
    elif isinstance(x, (list, tuple)) and fields:
        x = [dict((i, j[i]) for i in fields) for j in x]
    elif isinstance(x, dict) and fields:
        x = dict((i, x[i]) for i in fields)
    if as_json:
        x = json.dumps(x, default=json_default_encode)
    return x


def serialize_invoice(invoice, usettings, as_json=True):
    data = model_to_dict(invoice)
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
        'total__str': usettings.format_money(invoice.total)})
    tax_percent = invoice.tax * 100
    tax_str_format = '%d%%' if tax_percent.is_integer() else '%.2f%%'
    if invoice.client:
        data['client'] = invoice.client
        data['client_html'] = invoice.client.to_html()  # TODO: recursive serializer.
    data['tax_str'] = tax_str_format % tax_percent
    return serialize(data, as_json=as_json)
