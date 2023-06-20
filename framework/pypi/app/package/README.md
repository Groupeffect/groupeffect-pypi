# GROUPEFFECT-PYPI

Django app with rest framework integration for fast development.
Write task classes instead of management commands for faster cli integrations.
Run enhanced `startapp` command to generate boilerplate `ModeViewSets` from a configuration file.

https://github.com/Groupeffect/groupeffect-pypi/tree/main/framework/pypi/app/package


# Quick start

1. Add "groupeffect" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [ 
        ... 
        groupeffect,
        ...
    ]

`python manage.py makemigrations` -> add Namespace model 

`python manage.py migrate` -> migrates Namespace model 


## Requirements

- https://github.com/django/django

- https://www.django-rest-framework.org/

## Params in settings.py

`GROUPEFFECT_MANAGEMENT_TASKS` : List of classes, in STRING dot notation ( see: import_lib ) 

`GROUPEFFECT_CONFIG_JSON_FILE_PATH` : Json file path can be any Json content 

## Features ( Development status )

**Cli Commands**

- debug current configuration file, available tasks and cli options 

`python manage.py effect -d`

- help and usage

`python manage.py effect -h`

- create config file
    
    - in app folder, provide app name  
    
    `python manage.py effect -c create -t config -n api`
    
    - at certain path, provide path
    
    `python manage.py effect -c create -t config -p /app/package/tests/testapp/api`

- startapp with nested folders

    - from config file

    `GROUPEFFECT_CONFIG_JSON_FILE_PATH`

    `python manage.py effect -c app -t start -t config`


**Tasks** 

You can add task classes to the array. They will be called by the `effect` command and the `configuration` and `options` will be passed to the `__init__` function as `**context`. You can also find `Configurator` and `Command` classes in the `management.commands.effect` module. They will handle cli inputs, json file upload and task classes. Feel free to fit them to your needs.

Example: 

    settings.py:

    `GROUPEFFECT_MANAGEMENT_TASKS = ['app.module.script.class_name_1', app.module.script.task_class_2]`

    cli:

    `python manage.py effect`

    `python manage.py effect -c command_name_1 -command command_name_1 -t task_name_1 -task task_name_2`

The command and task names will be loaded to the task class under `self.tasks` and `self.commands` as list in the `MetaTask` class. You can subclass or overwrite the class to add custom processes depending on the cli inputs.

**Config json file**

You can add a global configuration file to your project which will be available in the
context of your task classes. It can be any json file. The purpose is to have a global
configuration for your custom task classes.

