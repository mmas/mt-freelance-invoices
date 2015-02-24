import re

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


class Invoice(models.Model):
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    number = models.CharField(max_length=100, unique=True)
    date_sent = models.DateTimeField(blank=True, null=True)  # Default=created.
    date_paid = models.DateTimeField(blank=True, null=True)
    client = models.ForeignKey(Client, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    pdf = models.FileField(upload_to=get_filename)
    daily_rate = models.FloatField(blank=True, null=True)
    status = models.IntegerField(default=0)  # (0|1|2)=(draft|sent|paid).

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return self.number

    # def save(self, **kwargs):
    #     if self.subtotal is not None and self.tax is not None:
    #         self.total = self.subtotal + self.tax
    #     if self.status == 'paid' and not self.date_paid:
    #         self.date_paid = timezone.now()
    #     return super(Invoice, self).save(**kwargs)


class Day(models.Model):
    date = models.DateField(unique=True)
    status = models.IntegerField(default=0)  # (nosel|selected|halfsel).
    invoice = models.ForeignKey(Invoice, related_name='days_worked', null=True)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return '%s' % self.date


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
