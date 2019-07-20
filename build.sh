#!/bin/bash

#python setup.py sdist upload -r pypi
twine upload dist/*gz
