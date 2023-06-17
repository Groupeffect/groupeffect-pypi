#!/bin/bash

# with simpel package
# cd /app/package && python -m build

# Update version number

rm -drf /app/package/dist
python /app/package/manage.py

# for django 
cd /app/package && python setup.py sdist
# create package manually
python -m twine upload --repository testpypi dist/* --verbose