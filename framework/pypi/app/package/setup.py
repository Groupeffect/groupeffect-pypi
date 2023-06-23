from setuptools import find_packages, setup

setup(
    name="groupeffect",
    include_package_data=True,
    description="A Django app for fast api development.",
    url="https://github.com/Groupeffect/groupeffect-pypi",
    author="Amir Yousefi",
    author_email="groupeffect.public@gmail.com",
    license="MIT",
    packages=find_packages(),
    package_data={
        "groupeffect": ["templates/*"],
    },
)
