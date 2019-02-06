# Setup MDB api
from setuptools import setup

setup(
    name='mdb',
    packages=['mdb'],
    include_package_data=True,
    install_requires=[
        'flask',
        'gitpython'
    ],
)
