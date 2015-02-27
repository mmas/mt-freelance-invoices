import re
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


def get_filename(instance, filename):
    return 'invoices/%s.%s' % (re.sub(r'\s+', '_', instance.number),
                               filename.split('.')[-1])


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
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    number = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(default=timezone.now())
    date_paid = models.DateTimeField(blank=True, null=True)
    client = models.ForeignKey(Client, null=True)
    subtotal = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    total = models.FloatField(default=0)
    pdf = models.FileField(upload_to=get_filename)
    daily_rate = models.FloatField(null=True)
    status = models.IntegerField(default=0)  # (0:draft|1:saved|2:sent|3:paid).
    created_from = models.IntegerField(default=0)  # (0:days|1:file).

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.number

    def _format_money(self, x, html=True):
        return '%s%.2f' % ('&pound;', x)  # TODO: store currency html

    def _format_date(self, x):
        return datetime.strftime(x, '%d/%m/%Y')  # TODO: store date format

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

    @property
    def days_worked_by_week(self, last_weekday=0):
        # last_weekday=(0:sunday|1:monday|...)
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
                    'week_ending_formatted': self._format_date(week_ending),
                    'total': self.daily_rate * day.day_worked}
                data.append(week)
            else:
                week['days_worked'] += day.day_worked
                week['total'] += self.daily_rate * day.day_worked
            week['total_html'] = self._format_money(week['total'])
        return data

    @property
    def date_formatted(self):
        return self._format_date(self.date)

    @property
    def tax_total(self):
        return self.subtotal * self.tax

    @property
    def subtotal_html(self):
        return self._format_money(self.subtotal)

    @property
    def tax_total_html(self):
        return self._format_money(self.tax_total)

    @property
    def total_html(self):
        return self._format_money(self.total)

    @property
    def daily_rate_html(self):
        return self._format_money(self.daily_rate)

    def save(self, **kwargs):
        if not self.number:
            self.number = self._get_new_number()
        if self.created_from_days:
            self.subtotal = self.days_worked_total * self.daily_rate
        self.total = self.subtotal * (1 + self.tax)
        if self.paid and not self.date_paid:
            self.date_paid = timezone.now()
        return super(Invoice, self).save(**kwargs)


class DayManager(models.Manager):

    def get_active_days(self):
        return self.get_queryset().all()  # TEMP
        # return self.get_queryset().exclude(status=3)


class Day(models.Model):
    date = models.DateField(unique=True)
    invoice = models.ForeignKey(Invoice, related_name='days_worked', null=True)
    half = models.BooleanField(default=False)
    saved = models.BooleanField(default=False)

    objects = DayManager()

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return '%s' % self.date

    @property
    def day_worked(self):
        if self.half:
            return .5
        else:
            return 1

    def save(self, **kwargs):
        if self.invoice:
            self.saved = True
        return super(Day, self).save(**kwargs)


class Settings(models.Model):
    email_address = models.CharField(max_length=100, blank=True)
    email_password = models.CharField(max_length=100, blank=True)
    email_smtp = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    company_address = models.TextField(blank=True)
    company_info = models.TextField(blank=True)
    company_account = models.CharField(max_length=50, blank=True)
    default_daily_rate = models.FloatField(default=0.)
    default_tax = models.FloatField(default=.2)  # [0,1].


class UserManager(BaseUserManager):

    def create_user(self, username, password, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, last_login=now, **extra_fields)
        user.set_password(password)
        user.settings = Settings.objects.create()
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
