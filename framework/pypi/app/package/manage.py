import os
import json


class VersionUpdate:
    def __init__(self) -> None:
        self.json_config = "/app/package/VERSION.json"
        self.config = None
        self.requirements = ""
        with open(self.json_config, "r") as f:
            self.config = json.load(f)

        with open(self.config["requirements"], "r") as f:
            for i in f.readlines():
                self.requirements += i

        self.version = self.config["version"]

    def cfg_config(self):
        return f"""[metadata]
name = groupeffect
version = {self.version}
description = A Django app to load dev stuff.
long_description = file: README.md
url = https://github.com/Groupeffect/groupeffect-pypi
author = {self.config["author"]}
author_email = {self.config["email"]}
license = MIT
classifiers =
    Environment :: Web Environment
    Framework :: Django
    Intended Audience :: Developers
    Operating System :: OS Independent
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
    Programming Language :: Python :: 3.10

[options]
include_package_data = true
packages = find:
python_requires = >=3.8
install_requires =
    {self.requirements}
    
"""

    def update_version(self):
        _v = self.version.split(".")
        minor = int(_v[2]) + 1
        self.version = f"{_v[0]}.{_v[1]}.{minor}"
        self.config["version"] = self.version

    def write_setup_cfg_update_version(self):
        self.update_version()
        print(self.cfg_config())
        with open(self.json_config, "w") as f:
            json.dump(self.config, f)
            f.close()

        with open(self.config["setup_cfg"], "w") as f:
            f.write(self.cfg_config())
            f.close()

    def test(self):
        self.write_setup_cfg_update_version()
        print(self.__dict__)


VersionUpdate().test()
