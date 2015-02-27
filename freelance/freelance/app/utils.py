import json
from datetime import datetime, date

from django.db.models import Model, QuerySet
from django.forms.models import model_to_dict


def json_default_encode(x):
    """Allow date and datetime JSON encoding."""
    if isinstance(x, (datetime, date)):
        return x.isoformat()
    elif isinstance(x, Model):
        return x.pk


def serialize(x, fields=[]):
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
    return json.dumps(x, default=json_default_encode)
