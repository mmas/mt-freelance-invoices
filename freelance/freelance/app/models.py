# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime
from cStringIO import StringIO

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.template import loader, Context

from xhtml2pdf.pisa import CreatePDF

from freelance.app.utils import serialize_invoice


def get_filename(instance, filename):
    return 'invoices/%s.pdf' % (re.sub(r'\s+', '_', instance.number))


class Currency(models.Model):
    name = models.CharField(max_length=70)
    code = models.CharField(max_length=3)

    class Meta:
        ordering = ('code',)

    def __unicode__(self):
        return '%s %s' % (self.code, self.name)


class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    email = models.EmailField()

    def __unicode__(self):
        return self.name

    def to_html(self):
        html = '<strong>%s</strong>' % self.name
        if self.address:
            html += '<br>%s' % self.address.replace('\n', '<br>')
        return html


class Invoice(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(default=timezone.now())
    date_paid = models.DateTimeField(blank=True, null=True)
    client = models.ForeignKey(Client, null=True)
    subtotal = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    total = models.FloatField(default=0)
    pdf = models.FileField(upload_to=get_filename, blank=True)
    daily_rate = models.FloatField(null=True)
    status = models.IntegerField(default=0)  # (0:draft|1:saved|2:sent|3:paid).
    created_from = models.IntegerField(default=0)  # (0:days|1:file).

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.number

    def _get_new_number(self):
        """Autoincreased number formatted as 'year+month+x' with max(x)=99."""
        now = timezone.now()
        for i in xrange(1, 100):
            number = '%04d%02d%02d' % (now.year, now.month, i)
            try:
                Invoice.objects.get(number=number)
            except Invoice.DoesNotExist:
                break
        return number

    def _create_pdf_from_days(self, usettings):
        tmp = StringIO()
        html = loader.get_template('invoice-pdf.html')
        ctx = serialize_invoice(self, usettings, as_json=False)
        ctx['static_root'] = settings.STATICFILES_DIRS[0]
        pdf = CreatePDF(html.render(Context(ctx)), tmp)

        if pdf.err:
            raise Exception('Error creating PDF file.')

        fname = get_filename(self, '').split('/')[-1]
        tmp.seek(0)
        self.pdf.save(fname,
                      SimpleUploadedFile(fname, tmp.read(), 'application/pdf'),
                      save=False)

    @property
    def saved(self):
        return self.status > 0

    @property
    def sent(self):
        return self.status == 2

    @property
    def paid(self):
        return self.status == 3

    @property
    def created_from_days(self):
        return self.created_from == 0

    @property
    def days_worked_dict(self):
        """Dict with the days worked (isodate:float)."""
        if self.created_from_days:
            return dict((i.date.isoformat(), i.day_worked)
                        for i in self.days_worked.all())

    @property
    def days_worked_total(self):
        """Sum of the days worked."""
        if self.created_from_days:
            return sum(self.days_worked_dict.values())

    def days_worked_by_week(self, usettings):
        # last_weekday=(0:sunday|1:monday|...)
        last_weekday = 0  # TODO: put in user settings.
        data = []
        for day in self.days_worked.all():
            y, w, _ = day.date.isocalendar()
            week = next((i for i in data if i['year'] == y and i['week'] == w),
                        None)
            if not week:
                week_ending = datetime.strptime(
                    '%d%d%d' % (y, w - 1, last_weekday), '%Y%W%w').date()
                week = {
                    'year': y,
                    'week': w,
                    'days_worked': day.day_worked,
                    'week_ending': week_ending,
                    'week_ending__str': usettings.format_date(week_ending),
                    'total': self.daily_rate * day.day_worked}
                data.append(week)
            else:
                week['days_worked'] += day.day_worked
                week['total'] += self.daily_rate * day.day_worked
            week['total__str'] = usettings.format_money(week['total'])
        return data

    @property
    def tax_total(self):
        return self.subtotal * self.tax

    def save_pdf(self, pdf):
        fname = get_filename(self, '').split('/')[-1]
        self.pdf.save(fname, pdf, True)

    def save(self, usettings=None, **kwargs):
        if not self.number:
            self.number = self._get_new_number()
        if self.created_from_days:
            self.subtotal = self.days_worked_total * self.daily_rate
        self.total = self.subtotal * (1 + self.tax)
        if self.paid and not self.date_paid:
            self.date_paid = timezone.now()
        elif self.date_paid and not self.paid:
            self.status = 3
        if not self.pdf and self.created_from_days and self.saved:
            self._create_pdf_from_days(usettings)
        return super(Invoice, self).save(**kwargs)

    def delete(self):
        """Delete the days worked if the invoice is a draft."""
        if not self.saved and self.days_worked.count():
            for day in self.days_worked.all():
                day.invoice = None
                day.save()
        if self.pdf:
            os.remove(self.pdf.path)
        return super(Invoice, self).delete()


class Day(models.Model):
    date = models.DateField(unique=True)
    invoice = models.ForeignKey(Invoice, related_name='days_worked', null=True)
    half = models.BooleanField(default=False)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return '%s' % self.date

    @property
    def day_worked(self):
        return .5 if self.half else 1


class Settings(models.Model):
    email_address = models.CharField(max_length=100, blank=True)
    email_smtp = models.CharField(max_length=100, default='smtp.gmail.com')
    email_smtp_port = models.IntegerField(default=587)
    email_protocol = models.IntegerField(
        default=0, choices=((0, 'tls'), (1, 'ssl')))
    company_name = models.CharField(max_length=100, blank=True)
    company_address = models.TextField(blank=True)
    company_info = models.TextField(blank=True)
    company_account = models.CharField(max_length=50, blank=True)
    default_daily_rate = models.FloatField(default=0.)
    default_tax = models.FloatField(default=.2)  # [0,1].
    date_format = models.CharField(max_length=50, default='%d/%m/%Y')
    currency = models.ForeignKey(Currency)

    def format_money(self, x):
        CURRENCY_MAP = {'GBP': '£',  # TODO: improve this.
                        'USD': '$',
                        'EUR': '€'}
        return '%s {:,.2f}'.format(x) % CURRENCY_MAP.get(self.currency.code,
                                                         self.currency.code)

    def format_date(self, x):
        return datetime.strftime(x, self.date_format)


class UserManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, last_login=now, **extra_fields)
        user.set_password(password)
        user.settings = Settings.objects.create(
            currency=Currency.objects.get(code='GBP'))
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        # Just defined to use the command-line
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    settings = models.OneToOneField(Settings, null=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()
