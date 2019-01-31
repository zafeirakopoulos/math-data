# Setup REST api
from setuptools import setup

setup(
    name='rest',
    packages=['rest'],
    include_package_data=True,
    install_requires=[
        'flask',
        'gitpython'
    ],
)