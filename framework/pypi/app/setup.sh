python /app/package/src/groupeffect/framework.py

cd /app/package && python -m build

# create package manually
# python -m twine upload --repository testpypi dist/*