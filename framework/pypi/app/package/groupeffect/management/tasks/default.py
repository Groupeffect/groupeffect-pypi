import os
from django.utils.module_loading import import_string
import shutil
from django.conf import settings
from django.core.management import call_command
from django.template.loader import get_template


class MetaTask:
    isAbstract = True

    def __init__(self, **context) -> None:
        self.GROUPEFFECT_MANAGEMENT_PATH = os.path.abspath(
            import_string("groupeffect.management").__file__,
        ).replace("__init__.py", "")
        self.context = context
        self.errors = []
        self.success = []
        self.configuration = context.get("configuration", None)
        self.options = context.get("options", None)
        self.status = [
            "\nCONFIGURATION:\n",
            context.get("configuration", None),
            "\nOPTIONS:\n",
            context.get("options", None),
        ]

        self.commands = None
        self.tasks = None
        if self.options:
            self.commands = self.options.get("command", None)
            self.tasks = self.options.get("task", None)
            self.noinput = self.options.get("noinput", False)

        # Will call run method if available
        if hasattr(self, "run"):
            getattr(self, "run")()

    def message(self, log, style="WARNING"):
        self.context["message"](getattr(self.context["style"], style)(log))


class DefaultTask(MetaTask):
    isAbstract = False

    def __init__(self, **context) -> None:
        self.result = {"create_config": []}
        super().__init__(**context)
        self.message(self.GROUPEFFECT_MANAGEMENT_PATH, "SUCCESS")
        self.status.insert(
            0,
            """\nYou can add Tasks by adding
GROUPEFFECT_MANAGEMENT_TASKS = ['app_name.module_name.script_name.class_name'] to your settings.py.\n""",
        )
        self.success += self.status


class CreateConfigurationJsonFileTask(MetaTask):
    """
    python manage.py effect -c create -t config -n api
    python manage.py effect -c create -t config -p /app/package/tests/testapp/api
    """

    def __init__(self, **context) -> None:
        super().__init__(**context)

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
    """
    Runs startpp command and adds folders and files to the app from GROUPEFFECT_CONFIG_JSON_FILE_PATH config json.

    python manage.py effect -c app -t start

    """

    def get_template(self, app, schema, service, model, name):
        path = os.path.join(
            self.GROUPEFFECT_MANAGEMENT_PATH.replace(
                "groupeffect/management", "groupeffect/templates"
            ),
            "groupeffect",
            schema,
            name + ".txt",
        )
        template = get_template(path)

        return template.render(
            {"app": app, "service": service, "model": model, "name": name}
        )

    def handle_config(self, config):
        app = config.get("app", "api")
        service = config.get("service", "service")
        model = config.get("model", "Organization")
        structure = config.get("structure", [])
        schema = config.get("schema", "default")

        call_command("startapp", app)

        for name in structure:
            folder = os.path.join(settings.BASE_DIR, app, name)
            if os.path.exists(folder):
                self.message(f"no changes to existing folder {folder}", "ERROR")
            else:
                os.makedirs(folder)
                self.message(f"created folder {folder}", "SUCCESS")

            file = os.path.join(settings.BASE_DIR, app, name, service + ".py")
            if os.path.exists(file):
                self.message(f"no changes to existing file {file}", "ERROR")
            else:
                with open(file, "w") as ff:
                    template = self.get_template(app, schema, service, model, name)
                    ff.write(template)
                    self.message(f"created file {file}", "SUCCESS")

    def startapp(self):
        self.message("### app START")
        for i in self.configuration:
            self.handle_config(i)

    def run(self):
        if self.commands:
            if "app" in self.commands and "start" in self.tasks:
                return self.startapp()
