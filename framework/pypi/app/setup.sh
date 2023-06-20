#!/bin/bash

# with simpel package
# cd /app/package && python -m build


rm -drf /app/package/dist
pip uninstall groupeffect -y
cp -r /app/package/tests/testapp/development/management /app/package/groupeffect/
## Update version number
# python /app/package/manage.py

## Build for django 
cd /app/package && python setup.py sdist
pip install /app/package/dist/*
## Upload package
# python -m twine upload --repository testpypi dist/* --verbose