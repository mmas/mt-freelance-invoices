import re

from django.db import models
from django.utils import timezone


def get_filename(instance, filename):
    return 'invoices/%s.%s' % (re.sub(r'\s+', '_', instance.number),
                               filename.split('.')[-1])


class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class Invoice(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    number = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)
    client = models.ForeignKey(Client)
    subtotal = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    file = models.FileField(upload_to=get_filename)
    status = models.CharField(max_length=10, default='draft')

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return self.number

    def save(self, **kwargs):
        if self.subtotal is not None and self.tax is not None:
            self.total = self.subtotal + self.tax
        if self.status == 'paid' and not self.date_paid:
            self.date_paid = timezone.now()
        return super(Invoice, self).save(**kwargs)
