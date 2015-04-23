#!/usr/bin/env python

from setuptools import *
setup(
    name='pea',
    version='0.1.1',
    author_email='tim3d.junk+pea@gmail.com',
    author='Tim Cuthbertson',
    url='http://github.com/gfxmonk/pea/tree',
    description="minimal BDD library",
    packages = find_packages(),
    entry_points = {
        'nose.plugins.0.10': ['pea = pea:PeaFormatter']
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
    ],
    keywords='test nosetests nose nosetest bdd cucumber lettuce',
    install_requires=[
        'setuptools',
        'nose',
        'python-termstyle',
        'colorama',
    ],
)
