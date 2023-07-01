# Meta Back-End Developer Capstone

If you have cloned this repo for grading I have taken the time to validate everything on my own project. I will guide you to what you need to look at to confirm. While there is a `Readme.txt` with the 2 endpoints we created for testing, that's all covered below in this `README.md` file.

First, in this directory you can `pipenv shell` to start a local virtual environment. Then run `pipenv install` or `pipenv update` to make sure the dependencies are satisfied. 

Second, make sure your `mysql` is started (I really need a startup script for this on my Codespace!). 

Third, move to the littlelemon directory to start the server `cd littlelemon` and `python manage.py runserver`.

## Review Criteria

Here are the criteria Coursera lists for grading.

* Does the web application use Django to serve static HTML content?

You will see that `django.contrib.staticfiles` is in the `INSTALLED_APPS` of the project package `settings.py` file. 

Additionally, `STATIC_URL = "static/"` is set in the `settings.py` file. 

This was tested during week 1 as the project folder `templates` folder contains the static files provided to us. 

Additionally, the restaurant app `static/restaurant` folder contains the `littlelemon.png` used during week 1. I renamed the `logo.png` since they didn't actually provide us the right file name! Other content in there was a copy of the zip file provided. 

* Has the learner committed the project to a Git repository?

You got this from GitHub, no? Yeah, I use a VCS. And GitHub Codespaces!

* Does the application connect the backend to a MySQL database?

See `settings.py` in the project package. I reused the same login credentials from the Full Stack course for my local MySQL instance. The full specification is copied here.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'littlelemon',
        'HOST' : '127.0.0.1',
        'PORT' : '3306',
        'USER' : 'admindjango',
        'PASSWORD' : 'employee@123!',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

* Are the menu and table booking APIs implemented?

I don't think we really tested the booking APIs in this course compared to the Full Stack course (and they're implemented differently). Nevertheless, see my `test.http` file in the restaurant application. Ensure your Visual Studio Code has the REST Client extension installed. You can simply click the "send request" button above each command to interact with the API.

Note, I did add a simple user test of the bookings API. Note, all endpoints do not have trailing slashes, per the requirements taught in the classes that APIs should not have them (so if you see an error, make sure you remove trailing slashes!).

In any case, you can also go to http://127.0.0.1:8000/restaurant/menu to see the running endpoint in the browsable interface.

* Is the application set up with user registration and authentication?

I have plenty of such tests in my API class project (ugh!), but yeah. Djoser is setup and pretty much out-of-the-box for this assignment. I didn't add the endpoint tests to this project, but feel free to try it out yourself (write it yourself or copy from APIs `requests` folder). 

You can also just use the admin interface (not as fun!). 

* Does the application contain unit tests?

See `test_models.py` and `test_views.py` in the restauranta app. And, of course, running `python manage.py test` will return you results. 

In my `test_views.py` I actually test 3 things (shoudl I do separate methods for each?). It validates the response code, the length of the response data object, and that the attributes match item-by-item.

Here is the output from my run.

```
(Capstone) @bryangoodrich ➜ /workspaces/coursera-meta-backend-littlelemon/Capstone/littlelemon (main) $ python manage.py test
Found 2 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.051s

OK
Destroying test database for alias 'default'...
```

* Can the API be tested with the Insomnia REST client?

I'm sure it can. I don't use Insomnia. I use the VS Code REST Client extension and write `.http` files to consolidate my interactive test scripts. See `test.http` in the restaurant application, per the earlier bullet. It's basically the same thing any REST client does without all the GUI and point-and-click I prefer to avoid. 