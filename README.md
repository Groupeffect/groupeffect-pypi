# Groupeffect
Pypi development project. Package Features are:
- Documentation
- Examples

`pip install groupeffect`

https://pypi.org/project/groupeffect/0.1.0/

# Docker Compose Workspace

`docker-compose up`
    
        - runs.sh : run server for interactive usage
        - setup.sh : create package dist


# Pypi

## Testing

- load test package:
    https://packaging.python.org/en/latest/tutorials/packaging-projects/
    `cd /app/test_package && python -m build`
    `python3 -m twine upload --repository testpypi dist/*`
    username = groupeffect

    Once uploaded, your package should be viewable on TestPyPI; for example: 
    - https://test.pypi.org/project/groupeffect-test/0.1.0/

    - install test package:
        `pip install -i https://test.pypi.org/simple/ groupeffect-test==0.1.0`

## Production

- load prod package:
    `cd /app/package && python -m build`
    `python -m twine upload dist/*`
    username = groupeffect    

    - install package:
        `pip install -i https://pypi.org/simple/ groupeffect==0.1.0`

