import os
from django.utils.module_loading import import_string
from django.conf import settings


class MetaTask:
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
