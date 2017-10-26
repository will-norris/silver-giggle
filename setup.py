import os

from setuptools import find_packages, setup

requires = [
    open(os.path.join('config', 'requirements.txt')).read()
]

setup(
    name='silver-giggle',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
