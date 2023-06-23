# Groupeffect: reusable Django app for developers

**Requirements**

- https://github.com/django/django

- https://www.django-rest-framework.org/

**Overview**

- Chain existing management commands in one cli command with the `effect -t m` command.
- Create boilerplate Django REST framework apps for fast development from configuration files and script templates with `effect -c app -t start`.
- Run multiple tasks with the same command in an array of tasks if you like. Write task classes instead of management commands for faster cli integrations.
- Custom configurations and templates can be implemented to create different boilerplate apps.
- The purpose is to create scripts and templates that can be controlled by management commands and the option to chain them together for a better workflow and development experience.
- The goal is to simplify complex processes or commands with automated task classes and allow them to trigger other processes with the django `call_command` function.   

**Contains**

- Management Command

`groupeffect.management.commands.effect`

- Task Classes

`groupeffect.management.tasks.default`
    
- Python script and Html templates 

`groupeffect.templates`
    

**This package is currently under development. Please don't be confused if something is wrong :)**

# Quick start

1. Add "groupeffect" to your INSTALLED_APPS setting like this:

    `INSTALLED_APPS = [ 
        ... 
        groupeffect,
        ...
    `]

    `python manage.py effect -d`
    `python manage.py effect -h`

    **THEN if you like to add a generic app**

2.  `python manage.py effect -c app -t start -n api`

    **OR**

    generate a config file in BASE_DIR folder with:

    `python manage.py effect -c create -t config`

    **THEN** 
    
    add `GROUPEFFECT_CONFIG_JSON_FILE_PATH` to settings.py

    **THEN** 

    `python manage.py effect -c app -t start`

3.  you have to import your models to `api.models.py` and include the `api.urls.organization` in your global url.py file in order to migrate the models and access the rest endpoints. 

### Params in settings.py

`GROUPEFFECT_MANAGEMENT_TASKS` : List of classes, in STRING dot notation ( see: import_lib ) 

`GROUPEFFECT_CONFIG_JSON_FILE_PATH` : Json file path can have any content as long you do not use the default tasks from the package.


### Boilerplate Task: CreateAppTask

Run enhanced `effect -c app -t start` command to generate a boilerplate app with models, serializers, views, urls and tests from a configuration file. The templates can be switched by the `schema` key in the config file. You can switch the templates if other schemas are available or you can subclass the `groupeffect.management.tasks.default.CreateAppTask` and overwrite `get_template` method for custom templates. Don't forget to add your task classes array to the settings.py file. You can also add your own configuration file. See the details below. Please let me know if something has to be explained better.

### Default config JSON file

You can add a global configuration file to your project which will be available in the context of your task classes see `groupeffect.management.task.default.CreatAppTask` if you use this task class then you have to keep the structure of the `default.json` file. But you can exclude the default task classes in your settings.py if you wish.

**A list with objects to add generic apps.**
**../groupeffect/management/configuration/default.json :**


    `[
        
        {

            "app": "api",
            "service":"organization",
            "model":"namespace",
            "structure": ["database","serializers", "views","urls", "tests"],
            "schema": "default"

        }

    ]`


Each dictionary entry must have a different app name otherwise the "app exists" error will be raised. You can change this behavior by overwriting the `handle_config` method of the `groupeffect.management.task.default.CreatAppTask` class. Currently I believe it would be better to prevent folders and files from being overwritten by the command.

**Description**:

    app:

        The django application name, default is api.
    
    service:

        The name of the nested scripts under the structured folders.
    
    model:

        The name of the django model class. It will be used to set the generic class names for the boilerplate templates and imports.

    structure:

        The folder names for nested namespaces and boilerplate template variables.

    schema:

        It is used for the folder name which contains the boilerplate templates.


# More Details

### Cli Commands

The cli command `python manage.py effect` is the minimum to run the `Command` class which is needed to run the task classes in an array. The available options are generic flags and can behave differently with different task classes. The task classes are responsible for the option input handling. The idea is that you can run multiple tasks with the same command if you want.

**debug log:**

current configuration available tasks and cli options 

`python manage.py effect -d`


**help: and usage**

`python manage.py effect -h`


**create: config file**

- in BASE_DIR folder  

    `python manage.py effect -c create -t config`

- in app folder 'api', provide app name with -n flag  

    `python manage.py effect -c create -t config -n api`

- at certain path, provide path

    `python manage.py effect -c create -t config -p /app/package/tests/testapp/api`


**start app with nested folders from config file**

- short

    `python manage.py effect -c app -t start`

- custom from cli 

    `python manage.py effect -c app -t start --name api --model Namespace --service organization --schema default`

**run multiple commands with `groupeffect.management.tasks.default.DefaultTask` class**

- help
    
    `python manage.py effect -t m`

    `python manage.py effect -t m -c help`

- list commands by index
    
    `python manage.py effect -t m -c list`

- chain available management commands by name or index

    `python manage.py effect -t m -c check -c makemigrations -c migrate -c collectstatic --noinput`

    `python manage.py effect -t m -c 1 -c 2 -c 3 ... --noinput` ( you must know the index from `effect -t m -c list` command )
        


### Tasks

Use the `groupeffect.management.tasks.default.MetaTask` to write new tasks. You can add task classes to the `GROUPEFFECT_MANAGEMENT_TASKS` array. They will be called by the `effect` command and the `configuration` and `options` will be passed to the `__init__` function as `**context`. You have to set the command and tasks functions in your `TaskClass` to handel stuff. You will also find a `Configurator` and a `Command` class in the `management.commands.effect` script. They will handle cli inputs, json file upload and task classes. Feel free to fit them to your needs. More details in cli commands. 

Example: 

    settings.py:

    `GROUPEFFECT_MANAGEMENT_TASKS = ['app.module.script.class_name_1', app.module.script.task_class_2]`

    cli:

    `python manage.py effect`

    `python manage.py effect -c command_name_y -command command_name_x -t task_name_1 -task task_name_2`

The command and task names will be loaded to the task class under `self.tasks` and `self.commands` as list in the `MetaTask` class. You can subclass or overwrite the class to add custom processes depending on the cli inputs.



**Package code on Github**

https://github.com/Groupeffect/groupeffect-pypi/tree/main/framework/pypi/app/package

**Development code on Github**

https://github.com/Groupeffect/groupeffect-pypi

**PyPi package**

https://pypi.org/project/groupeffect/

**Django package**

https://djangopackages.org/packages/p/groupeffect/


