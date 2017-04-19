# foodie


## Development setup

We use [Virtualenv](https://virtualenv.pypa.io/en/stable/) to manage different Python (we will be using python3) environments.


Retrieve our project
```
$ git clone https://github.com/wujunhua/foodie
$ cd foodies
```

Install dependencies in your environment
```
$ pip install -r requirements.txt
```

Install Postgres locally.

foodie/settings.py file will be storing database information. So we created a template for the settings file, /foodie/settings_sample.py. Copy this file to /foodie/settings.py and change the database info to match your database name, user, and password.

Make and run [migrations](https://docs.djangoproject.com/en/1.10/topics/migrations/)
```
$ python manage.py makemigrations
$ python manage.py migrate
```

Create Django superuser so you can access the admin portal
```
$ python manage.py createsuperuser
```

Start server
```
$ python manage.py runserver
```
