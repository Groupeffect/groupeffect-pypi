# Groupeffect
Pypi Project

# Pypi

https://test.pypi.org/project/groupeffect-test/0.1.0/

- load test package:
    https://packaging.python.org/en/latest/tutorials/packaging-projects/

    `python3 -m twine upload --repository testpypi dist/*`
    username = groupeffect

    Once uploaded, your package should be viewable on TestPyPI; for example: 
    - https://test.pypi.org/project/groupeffect-test/0.1.0/

- load prod package:
    `python -m build`
    `python -m twine upload dist/*`
    username = groupeffect    


- install test package:
    `pip install -i https://test.pypi.org/simple/ groupeffect-test==0.1.0`

- install test package:
    `pip install -i https://pypi.org/simple/ groupeffect==0.1.0`


# Docker

docker-compose up
    - runs.sh : run server for interactive usage
    - setup.sh : create package dist