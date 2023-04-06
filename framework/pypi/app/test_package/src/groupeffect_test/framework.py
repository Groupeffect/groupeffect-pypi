import os
from pprint import pprint


class MetaInfo:
    """Meta information class for current environment."""

    def __init__(self, PROJECT_ENVIRONMENT="DEFAULT") -> None:
        self.cwd = os.getcwd()
        self.PROJECT_ENVIRONMENT = os.getenv("PROJECT_ENVIRONMENT", PROJECT_ENVIRONMENT)
        self.environ = dict(os.environ)


if __name__ == "__main__":
    pprint(MetaInfo().__dict__)
