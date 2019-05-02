#!/bin/bash
exec pipenv run pytest --mypy --flake8 --isort --black interfaces $*
