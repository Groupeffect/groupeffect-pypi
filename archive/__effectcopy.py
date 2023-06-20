import os
import json
from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.conf import settings

GROUPEFFECT_EVENT_CHOICES = ["check", "create"]

GROUPEFFECT_CONFIG = [
    {
        "cli": True,
        "key": "event",
        "value": "check",
        "args": ["event"],
        "kwargs": {
            "type": str,
            "help": "Event name",
            "nargs": "?",
            "choices": GROUPEFFECT_EVENT_CHOICES,
        },
    },
    {
        "cli": True,
        "key": "command",
        "value": "info",
        "args": ["-c", "--command"],
        "kwargs": {
            "help": "Commando vocables are string seperated by single white space",
            "nargs": "?",
            "action": "append",
        },
    },
]

ATTRIBUTES = [i["key"] for i in GROUPEFFECT_CONFIG]


class Configurator:
    def __init__(self) -> None:
        self.effect_success = []
        self.effect_errors = []
        self.config_file = None
        # add env variable for json file or add a json file at BASE_DIR named groupeffect.json
        try:
            self.config_file = settings.GROUPEFFECT_CONFIG_JSON_FILE_PATH
        except Exception as e:
            self.effect_errors.append(e)
        if not self.config_file:
            self.config_file = os.getenv(
                "GROUPEFFECT_CONFIG_JSON_FILE_PATH",
                os.path.join(settings.BASE_DIR, "groupeffect.json"),
            )

        self.effect_register = []
        self.effect_config = None
        self.effect_setup = []  # GROUPEFFECT_CONFIG
        self.allowed_multiple_keys = ["add_model"]
        self.read_config_json()
        self.cls_attributes = ATTRIBUTES
        # self.setup_check()

    def read_config_json(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.effect_config = json.load(f)
        else:
            self.effect_errors.append(
                f"{self.config_file} does not exists. You can add this file manually if you want."
            )

    def check_option(self, key, value):
        # if key in ["name", "full", "debug"]:
        if value is not None:
            data = {"key": key, "value": value}
            self.effect_register.append(data)

    def check_input(self, options):
        print(options)
        for i in options:
            self.check_option(i, options[i])

    def consolidate_config(self):
        """
        Load groupeffect.json if available then check cli inputs then combine them.
        Cli input overwrites groupeffect.json config object
        """
        key_check = []
        value_check = []
        if self.effect_config:
            for config in self.effect_config:
                if config["key"] not in [x["key"] for x in self.effect_register]:
                    if config["key"] not in key_check:
                        key_check.append(config["key"])
                        self.effect_setup.append(config)
                    elif config["key"] in self.allowed_multiple_keys:
                        if config["value"] not in value_check:
                            value_check.append(config["value"])
                            self.effect_setup.append(config)
                        else:
                            raise Exception(
                                f"Error multiple identical config values in {self.config_file}: {config}"
                            )

                    else:
                        raise Exception(
                            f"Error multiple identical config keys in {self.config_file}: {config}"
                        )
        else:
            self.effect_errors.append("NO CONFIG !")

        if self.effect_register:
            for config in self.effect_register:
                self.effect_setup.append(config)

        # set attributes for write actions
        for config in self.effect_setup:
            if config["key"] in self.cls_attributes:
                setattr(self, f"app_{config['key']}", config["value"])

    def setup_check(self):
        for config in self.effect_setup:
            self.effect_success.append(config)

        if not hasattr(self, "app_event"):
            self.effect_errors.append(
                f"event is missing. Use: python manage.py effect {GROUPEFFECT_EVENT_CHOICES} -c <string>"
            )

    def effect(self, options):
        self.check_input(options)
        self.consolidate_config()
        self.setup_check()


class Command(BaseCommand):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = None
        self.effect_setup = None
        self.effect_success = None
        self.effect_errors = None
        # self.config_file = None
        # # add env variable for json file or add a json file at BASE_DIR named groupeffect.json
        # try:
        #     self.config_file = settings.GROUPEFFECT_CONFIG_JSON_FILE_PATH
        # except Exception as e:
        #     self.effect_errors.append(e)
        # if not self.config_file:
        #     self.config_file = os.getenv(
        #         "GROUPEFFECT_CONFIG_JSON_FILE_PATH",
        #         os.path.join(settings.BASE_DIR, "groupeffect.json"),
        #     )

        # self.effect_register = []
        # self.effect_config = None
        # self.effect_setup = []
        # self.allowed_multiple_keys = ["add_model"]

    def create_parser(
        self, prog_name: str, subcommand: str, **kwargs: Any
    ) -> CommandParser:
        print("##### CETU")
        print(prog_name)
        print(subcommand)
        print(kwargs)
        self.config = Configurator()
        self.config.effect(kwargs)
        self.effect_setup = self.config.effect_setup
        self.effect_success = self.config.effect_success
        self.effect_errors = self.config.effect_errors

        return super().create_parser(prog_name, subcommand, **kwargs)

    def add_arguments(self, parser: CommandParser) -> None:
        print("### ADDINg")
        self._parser = parser
        for config in self.effect_setup:
            if "cli" in config and config["cli"]:
                if "args" in config and "args" in config:

                    self._parser.add_argument(*config["args"], **config["kwargs"])

    def handle(self, *args, **options) -> str | None:

        # try:
        #     self.effect(options)
        # except Exception as e:
        #     self.effect_errors.append(e)

        for i in self.effect_success:
            self.stdout.write(self.style.SUCCESS(str(i)))
        for i in self.effect_errors:
            self.stdout.write(self.style.ERROR(str(i)))

        if self.effect_errors:
            self._parser.print_usage()
