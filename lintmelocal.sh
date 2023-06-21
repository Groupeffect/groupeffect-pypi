#!/bin/bash
# Superlinter
# Local development linter uses git worflow actions 
# https://github.com/marketplace/actions/super-linter

# remove py cache

FOLDER=~/projects/github/groupeffect-pypi
CONFIG_FILE_NAME=superlinter.yml
CONFIG_FILE_PATH=$FOLDER/.github/workflows/$CONFIG_FILE_NAME
podman run --rm \
    -e RUN_LOCAL=true \
    -e VALIDATE_DOCKERFILE_HADOLINT=false \
    -e VALIDATE_NATURAL_LANGUAGE=false \
    -e VALIDATE_PYTHON_FLAKE8=false \
    -e VALIDATE_PYTHON_ISORT=false \
    -e VALIDATE_PYTHON_MYPY=false \
    -e USE_FIND_ALGORITHM=true \
    -e VALIDATE_GITLEAKS=false \
    -e VALIDATE_MARKDOWN=false \
    -e VALIDATE_HTML=false \
    -e VALIDATE_BASH=false \
    -v $FOLDER:/tmp/lint github/super-linter

    # -e YAML_CONFIG_FILE=$CONFIG_FILE_NAME \
    # -v $CONFIG_FILE_PATH:/action/lib/.automation/$CONFIG_FILE_NAME \