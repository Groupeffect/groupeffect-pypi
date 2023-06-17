# GROUPEFFECT

development stuff

https://github.com/Groupeffect/groupeffect-pypi/tree/main/framework/pypi/app/package


## Django app for fast development

Quick start
-----------

1. Add "groupeffect" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "groupeffect",
    ]

2. Include the groupeffect URLconf in your project urls.py like this::

    path("", include("groupeffect.urls.main"))