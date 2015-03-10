#mt-freelance-invoices
Web app for freelancers to manage invoices. Create invoices easily directly from day-based timesheets. Download your invoices. Send directly the invoice in pdf to the client just with one click.

![Image](http://www.mastortosa.com/media/images/freelance_invoices__06.png)

##Requirements

  - Web server(eg: [apache](https://httpd.apache.org/))
  - Database (eg: [postgresql](http://www.postgresql.org/))
  - [Virtualenv](https://virtualenv.pypa.io/en/latest/)

##Installation in your server (debian-based)
\* Assume SERVER_NAME like invoices.myweb.com

```
$ cd /var/www
$ git clone https://github.com/mastortosa/mt-freelance-invoices.git
$ mv mt-freelance-invoices SERVER_NAME
$ cd freelance
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ cd freelance
$ mkdir media && chown -R www-data:www-data media
```

Get a secret key:

```
$ python
>>> import base64, uuid
>>> base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
'mqKWbFz6RrWwhMIie+Rb/9eU5GR5cUCIq4SsKuju5Rw='
```

Edit your settings. You will need to set, at least, the SECRET_KEY, DATABASE.NAME, DATABASE.USER, DATABASE.PASSWORD and ALLOWED_HOSTS:
```
$ cp settings_server.example.py settings_server.py
$ nano settings_server.py
```

Create and set up the the database:

```
$ createdb freelance
$ cd freelance
$ python manage.py syncdb --noinput
$ python manage.py loaddata data.json
$ python manage.py createsuperuser
```

Set up the server (example using apache):

```
nano /etc/apache2/sites-available/SERVER_NAME
```

```
<VirtualHost *:80>
    ServerName SERVER_NAME

    DocumentRoot /var/www/SERVER_NAME/freelance

    WSGIDaemonProcess freelance python-path=/var/www/SERVER_NAME/freelance:/var/www/SERVER_NAME/venv/lib/python2.7/site-packages
    WSGIProcessGroup freelance
    WSGIScriptAlias / /var/www/SERVER_NAME/freelance/freelance/wsgi.py

    Alias /static/ /var/www/SERVER_NAME/freelance/freelance/app/ui/static/
    Alias /media/ /var/www/SERVER_NAME/freelance/freelance/media/
    Alias /robots.txt /var/www/SERVER_NAME/robots.txt

    ErrorLog /var/log/apache2/freelance.error.log
    CustomLog /var/log/apache2/freelance.access.log combined
</VirtualHost>
```

```
$ a2ensite SERVER_NAME
$ service apache2 start
```

![Image](http://www.mastortosa.com/media/images/freelance_invoices__01.png)