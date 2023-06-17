# GROUPEFFECT-PYPI

Django app with rest framework integration for fast development

`https://github.com/Groupeffect/groupeffect-pypi/tree/main/framework/pypi/app/package`


## Django integration

Quick start
-----------

1. Add "groupeffect" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "groupeffect",
    ]

2. Include the groupeffect URLconf in your project urls.py like this::

    path("", include("groupeffect.urls.main"))

3. Commands 

`python manage.py makemigrations`

`python manage.py migrate`


- https://github.com/django/django

- https://www.django-rest-framework.org/

## Features

- Standard command for setting up apps with rest endpoints:

`python manage.py effect` -> help and usage

`python manage.py effect start <app name>`

`python manage.py effect start <app name> -f <config json file path>`

### Config json file

Definition:

`
{
    "app_name": "string" # is required
    "add_models": "string_bool [True , False]" # is optional default is False
    "add_views"
}
`

Example:

`
{
    "app_name": "api", 
    "add_models": "True",
    "add_views": ""
}
`
