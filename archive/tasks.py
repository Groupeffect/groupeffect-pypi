import os
import shutil
from typing import Any, List, Dict
from logging import getLogger
from django.conf import settings
from development.management.tasks.default import MetaTask
from django.core.management import call_command
from django.template.loader import get_template

logger = getLogger(__name__)


class CreateConfigurationJsonFileTask(MetaTask):
    """
    python manage.py effect -c create -t config -n api
    python manage.py effect -c create -t config -p /app/package/tests/testapp/api
    """

    def __init__(self, **context) -> None:
        super().__init__(**context)
        self.run()

    def run(self):
        if self.commands:
            if "create" in self.commands:
                if self.tasks:
                    if "config" in self.tasks:
                        self.message("# Creating config")

                        path_to_app = self.options.get("path", None)
                        app_name = self.options.get("name", None)
                        path = None
                        if path_to_app:
                            path = path_to_app
                        elif app_name:
                            path = os.path.join(settings.BASE_DIR, app_name)
                        else:
                            path = settings.BASE_DIR

                        path = os.path.join(path, "default.json")
                        if not os.path.exists(path):
                            default = os.path.join(
                                self.GROUPEFFECT_MANAGEMENT_PATH,
                                "configuration/default.json",
                            )

                            shutil.copy(default, path)
                        else:
                            self.message(f"Config file already exists: {path}")
                            self.errors.append(
                                f"command error: create config: file already exists: {path}"
                            )


class CreateAppTask(MetaTask):
    def startapp(self):
        self.message("### app START")
        template = get_template("scripts/default/serializers.txt")
        print(template.render({"model": "TTTTEST"}))

    def updateapp(self):
        pass

    def run(self):
        if self.commands:
            if "app" in self.commands:
                if self.tasks:
                    if "start" in self.tasks:
                        return self.startapp()
                    elif "update" in self.tasks:
                        return self.updateapp()


class ___CreateAppTask(MetaTask):
    def __init__(self, **context) -> None:
        super().__init__(**context)
        self.message(f"# ok {self.__class__}")

        if self.options["debug"]:
            p = "/app/package/tests/testapp/api"
            if os.path.exists(p):
                shutil.rmtree(p)

        self.run()

    def get_template(self, name, config):
        template = None
        schema = "default"

        if "schema" in config:
            schema = config["schema"]

        file_template = os.path.join(
            self.GROUPEFFECT_MANAGEMENT_PATH,
            "templates",
            schema,
            name + ".py",
        )
        self.message(config)
        prefix = self.options.get("prefix", "GroupeffectNamespace")
        if not prefix:
            prefix = "GroupeffectNamespace"
        _imports = ""
        if name in ["database"]:
            pass
        elif name in ["serializers"]:
            _imports = f"from {config['app']}.{name}.{config['service']} import {config['service'].title()}\n"

        elif name in ["views"]:
            _imports = f"from {config['app']}.{name}.{config['service']} import {config['service'].title()}ModelSerializer\n"

        elif name in ["urls"]:
            _imports = f"from {config['app']}.{name}.{config['service']} import {config['service'].title()}ModelViewSet\n"

        with open(file_template, "r") as f:
            string = _imports
            for i in f.readlines():
                string += i.replace(prefix, config["service"].title())

            template = string
        return template

    def create_folders(self, config):
        for f in config["structure"]:
            folder = os.path.join(settings.BASE_DIR, config["app"], f)
            if os.path.exists(folder):
                self.message(f"no changes to existing folder {folder}", "ERROR")
            else:
                os.makedirs(folder)
                self.message(f"created folder {folder}", "SUCCESS")

    def create_files(self, config):
        for f in config["structure"]:
            file = os.path.join(
                settings.BASE_DIR, config["app"], f, config["service"] + ".py"
            )
            if os.path.exists(file):
                self.message(f"no changes to existing file {file}", "ERROR")
            else:
                with open(file, "w") as ff:
                    ff.write(self.get_template(f, config))
                    self.message(f"created file {file}", "SUCCESS")

    def create(self):
        for i in self.configuration:
            try:
                call_command("startapp", i["app"])
            except Exception as e:
                self.errors.append(e)
            self.create_folders(i)
            self.create_files(i)

    def startapp(self):
        self.message("# START NEW APP")
        self.success.append("# START NEW APP")

        if "config" in self.tasks:
            if self.configuration:
                self.message(self.configuration)
                self.create()
            else:
                self.message("No configuration found", "ERROR")
        return True

    def updateapp(self):
        self.message("# UPDATE APP")
        return True

    def run(self):
        if self.commands:
            if "app" in self.commands:
                if self.tasks:
                    if "start" in self.tasks:
                        return self.startapp()
                    elif "update" in self.tasks:
                        return self.updateapp()


class __TestTask(MetaTask):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.noinput = self.options["noinput"]
        self.startapp()
        self.read_tasks()

    def get_paths(self, path_to_app, labels):
        return [os.path.join(path_to_app, i) for i in labels]

    def interactive(self, info, options=["y", "n"]):
        # INTERACTIVE PROMPT OR NO INPUT
        if self.noinput:
            return False
        value = None
        while value not in options:
            print('\nMust be "y" or "n" input')
            value = input(f"{info}\noptions: {options}\n>> ")

        if value == "y":
            return True
        elif value == "n":
            return False
        elif value in options:
            return value

        return False

    def check_folders(self, paths):
        for f in paths:
            if os.path.exists(f):
                overwrite = self.interactive(info=f"Overwrite {f} ?")

    def check_files(self, paths):
        # check and create files
        for f in paths:
            if os.path.exists(f):
                overwrite = self.interactive(f"Overwrite {f} ?")
            # Create file
            else:
                print(f"####### else {f}")
                # with open(f, "w") as file:
                #     file.write(f"# EFFECT {f}")
                #     file.close()

    def structure(self, path_to_app):

        startapp_files = self.get_paths(
            path_to_app,
            [
                "models.py",
                "views.py",
                "urls.py",
                "tests.py",
            ],
        )
        folders = self.get_paths(
            path_to_app,
            [
                "database",
                "serializers",
                "views",
                "urls",
                "tests",
            ],
        )
        effect_files = [
            os.path.join(i, f"{self.options['service']}.py") for i in folders
        ]

        self.check_files(startapp_files)
        self.check_folders(folders)
        self.check_files(effect_files)

    def startapp(self):
        if self.commands:
            if "startapp" in self.commands:
                if not self.options["name"]:
                    self.options["name"] = input(
                        "Set app name or leave blank for default = 'api'\n>> "
                    )
                    if not self.options["name"]:
                        self.options["name"] = "api"

                if "service" not in self.options:
                    self.options["service"] = input(
                        "Set app service or leave blank for default = 'service'\n>> "
                    )
                    if not self.options["service"]:
                        self.options["service"] = "service"

                # raise Exception("Set --name <string> value for your new app.")
                self.success.append("## Creating full app")
                try:
                    call_command("startapp", self.options["name"])
                except Exception as e:
                    self.errors.append(e)
                # Check
                path_to_app = os.path.join(settings.BASE_DIR, self.options["name"])
                if os.path.exists(path_to_app):
                    self.structure(path_to_app)

    def read_tasks(self):
        if self.commands:
            if "startapp" in self.commands:
                return None
        if self.tasks:
            if "model" in self.tasks:
                if "save" in self.tasks:
                    self.success.append("\n## Creating model")
                else:
                    print("TEMPLATE")

            if "serializer" in self.tasks:
                self.success.append("\n## Creating serializer")
            if "view" in self.tasks:
                self.success.append("\n## Creating view")
            if "url" in self.tasks:
                self.success.append("\n## Creating url")
