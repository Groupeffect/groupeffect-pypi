import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.utils.module_loading import import_string


GROUPEFFECT_CLI_OPTIONS = [
    {
        "key": "command",
        "value": "info",
        "args": ["-c", "--command"],
        "kwargs": {
            "help": "Commando vocables are string seperated by single white space",
            "nargs": "?",
            "action": "append",
        },
    },
    {
        "key": "task",
        "value": "default",
        "args": ["-t", "--task"],
        "kwargs": {
            "type": str,
            "help": "Task name. You can use it multiple times like -t X -t Y",
            "nargs": "?",
            "action": "append",
        },
    },
    {
        "key": "debug",
        "value": "0",
        "args": ["-d", "--debug"],
        "kwargs": {
            "help": "For test or debug set -t flag",
            "action": "store_true",
        },
    },
    {
        "key": "info",
        "value": "0",
        "args": ["-i", "--info"],
        "kwargs": {
            "help": "Info name",
            "action": "store_true",
        },
    },
    {
        "key": "noinput",
        "value": "0",
        "args": ["-ni", "--noinput"],
        "kwargs": {
            "help": "Non interactive command flag",
            "action": "store_true",
        },
    },
    {
        "key": "name",
        "value": "api",
        "args": ["-n", "--name"],
        "kwargs": {
            "nargs": "?",
            "help": "Name value",
        },
    },
    {
        "key": "model",
        "value": "Namespace",
        "args": ["-mo", "--model"],
        "kwargs": {
            "nargs": "?",
            "help": "Model name",
        },
    },
    {
        "key": "schema",
        "value": "default",
        "args": ["-sc", "--schema"],
        "kwargs": {
            "nargs": "?",
            "help": "Schema name",
        },
    },
    {
        "key": "service",
        "value": "api",
        "args": ["-s", "--service"],
        "kwargs": {
            "nargs": "?",
            "help": "Service name",
        },
    },
    {
        "key": "path",
        "value": "api",
        "args": ["-p", "--path"],
        "kwargs": {
            "nargs": "?",
            "help": "Path to something",
        },
    },
    {
        "key": "prefix",
        "value": "api",
        "args": ["-pf", "--prefix"],
        "kwargs": {
            "nargs": "?",
            "help": "Prefix for something",
        },
    },
    {
        "key": "argument",
        "value": "argument",
        "args": ["-a", "--argument"],
        "kwargs": {
            "nargs": "?",
            "help": "Argument for something",
            "action": "append",
        },
    },
]


class Configurator:
    def __init__(self, options=None) -> None:
        self.success = []
        self.errors = []
        self.config_file = None
        self.configuration = "No config file"
        self.options = options

        try:
            self.config_file = settings.GROUPEFFECT_CONFIG_JSON_FILE_PATH
        except Exception as e:
            self.errors.append(e)

        if not self.config_file:
            default = os.path.abspath(
                import_string("groupeffect.management").__file__
            ).replace("__init__.py", "configuration/default.json")

            self.config_file = os.getenv(
                "GROUPEFFECT_CONFIG_JSON_FILE_PATH",
                default,
            )
        self.read_config_json()

        self.tasks = [
            import_string("groupeffect.management.tasks.default.DefaultTask"),
            import_string("groupeffect.management.tasks.default.CreateAppTask"),
            import_string(
                "groupeffect.management.tasks.default.CreateConfigurationJsonFileTask"
            ),
        ]
        try:
            self.tasks = [
                import_string(i) for i in settings.GROUPEFFECT_MANAGEMENT_TASKS
            ]
            self.success.append(
                """
You changed the default tasks they are no longer available.
If you want to keep the default tasks.
you can add:

    groupeffect.management.tasks.default.DefaultTask,
    groupeffect.management.tasks.default.CreateAppTask,
    groupeffect.management.tasks.default.CreateConfigurationJsonFileTask,

to:

GROUPEFFECT_MANAGEMENT_TASKS

"""
            )
        except Exception as e:
            self.errors.append(e)

        if not self.tasks:
            self.errors.append("No tasks found")

    def read_config_json(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.configuration = json.load(f)
        else:
            self.errors.append(
                f"""{self.config_file} does not exists. You can add this file manually if you want.
Or add GROUPEFFECT_CONFIG_JSON_FILE_PATH to your settings.py"""
            )


class Command(BaseCommand):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.success = []
        self.errors = []
        self.configurator = Configurator
        self.cli_options = GROUPEFFECT_CLI_OPTIONS

    def add_arguments(self, parser: CommandParser) -> None:
        # https://docs.python.org/3/library/argparse.html#action
        for config in self.cli_options:
            if "args" in config and "kwargs" in config:
                parser.add_argument(*config["args"], **config["kwargs"])

    def handle(self, *args, **options) -> str | None:
        # Setup configurator
        self.config = self.configurator(options)

        # Run tasks
        for i in self.config.tasks:
            task = i(
                **{
                    "configuration": self.config.configuration,
                    "options": options,
                    "message": self.stdout.write,
                    "style": self.style,
                }
            )
            self.success += task.success
            self.errors += task.errors

        # Add messages
        self.success += self.config.success
        self.success += ["\nTASKS:\n", str(self.config.tasks)]
        self.errors += self.config.errors

        if options["debug"]:
            for i in self.success:
                self.stdout.write(str(i))
            for i in self.errors:
                self.stdout.write(self.style.ERROR(str(i)))
