# Groupeffect

This project is a workflow configuration to setup python packages in a dockerized environment.

It contains a pypi package and development scripts to push test and prod packages.

The main pypi package is saved under `framework/pypi/app/package/groupeffect`

The package README.md can be found under:

https://github.com/Groupeffect/groupeffect-pypi/blob/main/framework/pypi/app/package/README.md

## Docker environment

docker-compose or podman-compose up 

- `podman-compose build`

- `podman-compose -f docker-compose.yaml up`

- `podman-compose -f docker-compose.yaml up --build --remove-orphans`

- `framework/pypi/app/run.sh` : run server for interactive usage

- `framework/pypi/app/setup.sh` : create package dist and push to test.pypi

## Pypi

Always update version number !!!

use `framework/.pypirc` for pypi and twine authentication

see example `framework/.pypirc_example`

**Packaging**

- https://packaging.python.org/en/latest/tutorials/packaging-projects/

**Test package**

load test package:

- use setup.cfg for django apps

`python setup.py sdist`

`python3 -m twine upload --repository testpypi dist/*`

Once uploaded, your package should be visible on TestPyPI; for example: 

- https://test.pypi.org/project/groupeffect/0.1.0/


- install test package:

`pip install -i https://test.pypi.org/simple/ groupeffect==0.1.*`

- Test the app in django test project:

go to:

`framework/pypi/app/package/tests/testapp`

and run django commands:

`python manage.py makemigrations`

`python manage.py migrate`

**Production**

- load prod package:

use setup.cfg for django apps

`python setup.py sdist`

OR

use pyproject.toml for regular packages

`python -m build`

THEN

`python -m twine upload dist/*`

- install prod package:

`pip install groupeffect`


