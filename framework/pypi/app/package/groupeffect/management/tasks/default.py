import os
import shutil
from django.conf import settings
from django.core.management import call_command, get_commands
from django.template.loader import get_template
from django.utils.module_loading import import_string


class MetaTask:
    isAbstract = True

    def __init__(self, **context) -> None:
        self.GROUPEFFECT_MANAGEMENT_PATH = os.path.abspath(
            import_string("groupeffect.management").__file__,
        ).replace("__init__.py", "")
        self.context = context
        self.errors = []
        self.success = []
        self.configuration = context.get("configuration", {})
        self.options = context.get("options", {})
        self.status = [
            "\nCONFIGURATION:\n",
            context.get("configuration", None),
            "\nOPTIONS:\n",
            context.get("options", None),
        ]

        self.commands = self.options.get("command", [])
        self.tasks = self.options.get("task", [])
        self.arguments = self.options.get("argument", [])
        self.noinput = self.options.get("noinput", False)

        # Will call run method if available
        if hasattr(self, "run"):
            getattr(self, "run")()

    def message(self, log, style="WARNING"):
        if style is None:
            self.context["message"](log)
        else:
            self.context["message"](getattr(self.context["style"], style)(log))


class DefaultTask(MetaTask):
    isAbstract = False
    examples = """
Chain multiple commands. The order is important.

Syntax:
python3 manage.py effect <--task | -t> <multi | m> <--command | -c> <INDEX | NAME> -c ...

Example 1:
python3 manage.py effect -t multi -c makemigrations -c migrate -c collectstatic --noinput

Example 2:
python3 manage.py effect -t m -c flush -c makemigrations -c migrate -c collectstatic -c runserver --ni

EXAMPLE 3:
short form if you know the indexes of the commands:
python3 manage.py effect -t m -c 0 -c makemigrations -c 1 -c 2 -c 3 -c 4 -c 5 ...

PASS ARGUEMENTS WITH <--argument | -a> flag:
Use arguments with caution all commands will receive the arguments during the call_command(*[command, arg-1, arg-2 ...])

EXAMPLE 4:
Mix index and names with arguements:
python3 manage.py effect -t m -c check -a api -c 17 # 17 is makemigrations in my case and app label is api

INDEX LIST:
python3 manage.py effect -t m -c l
python3 manage.py effect -t multi -c list
python3 manage.py effect -t m

"""

    def __init__(self, **context) -> None:
        self.system_commands = {}
        self.default_commands = {}
        super().__init__(**context)
        self.message(self.GROUPEFFECT_MANAGEMENT_PATH)
        self.status.insert(
            0,
            """\nYou can add Tasks by adding
GROUPEFFECT_MANAGEMENT_TASKS = ['app_name.module_name.script_name.class_name'] to your settings.py.\n""",
        )
        self.success += self.status

    def set_meta_commands(self):
        self.message("CREATE: RUN LIST", "WARNING")
        self.default_commands = get_commands()
        for command in enumerate(sorted(self.default_commands.keys())):
            self.system_commands[str(command[0])] = command[1]

        self.success.append(sorted(self.system_commands))

    def run_help_message(self, examples=True):
        self.message("HELP : RUN COMMAND LIST", "SUCCESS")
        self.message("INDEX: COMMAND", "NOTICE")
        for i in self.system_commands:
            self.message(
                f"'{i}': {self.system_commands[i]}",
                "NOTICE",
            )
        if examples:
            self.message(self.examples, None)

    def __call_command__(self, key):
        args = [key]

        if self.noinput:
            args.append("--noinput")
        if self.arguments:
            self.message(self.arguments, "SUCCESS")
            self.message(
                "Use arguments carefully they will be called with each command.",
            )
            for argument in self.arguments:
                args.append(argument)
        try:
            call_command(*args)
        except Exception as e:
            self.errors.append(e)
            call_command(key)

    def run(self):
        """Chain existing commands in one command"""
        if self.tasks:
            if "multi" in self.tasks or "m" in self.tasks:
                self.set_meta_commands()
                if self.commands:
                    if "help" in [*self.tasks, *self.commands] or "h" in [
                        *self.tasks,
                        *self.commands,
                    ]:
                        self.run_help_message()

                    elif "l" in self.commands or "list" in self.commands:
                        self.run_help_message(examples=False)

                    elif self.default_commands:
                        for command in self.commands:
                            if command in self.system_commands:
                                self.message(command)
                                self.__call_command__(self.system_commands[command])

                            elif command in self.default_commands.keys():
                                self.__call_command__(command)
                            else:
                                self.message(command, "ERROR")
                                self.message(type(command), "ERROR")

                else:
                    self.run_help_message()


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
        app, service, model, schema = (
            self.options.get("name"),
            self.options.get("service"),
            self.options.get("model"),
            self.options.get("schema"),
        )

        app = app if app else config.get("name", "api")
        service = service if service else config.get("service", "organization")
        model = model if model else config.get("model", "Namespace")
        schema = schema if schema else config.get("schema", "default")
        structure = config.get("structure", [])

        call_command("startapp", app)

        for name in structure:
            folder = os.path.join(settings.BASE_DIR, app, name)
            if os.path.exists(folder):
                self.message(f"no changes to existing folder {folder}", "ERROR")
            else:
                os.makedirs(folder)
                self.message(f"created folder {folder}", "SUCCESS")

                # important for python processes
                # create __init__.py file in folder if not exist
                init_file_path = os.path.join(folder, "__init__.py")
                if not os.path.exists(init_file_path):
                    with open(init_file_path, "w") as ff:
                        ff.write("### auto generated by groupeffect ###")
                        ff.close()

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
