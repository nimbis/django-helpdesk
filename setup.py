from __future__ import print_function

import os
import sys
from distutils.util import convert_path
from fnmatch import fnmatchcase
from setuptools import setup, find_packages

version = '0.2.6+nimbis.12'

# Provided as an attribute, so you can append to these instead
# of replicating them:
standard_exclude = ('*.py', '*.pyc', '*$py.class', '*~', '.*', '*.bak')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build',
                                './dist', 'EGG-INFO', '*.egg-info')

# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
# Note: you may want to copy this into your setup.py file verbatim, as
# you can't import this from another package, when you don't know if
# that package is installed yet.
def find_package_data(
    where='.', package='',
    exclude=standard_exclude,
    exclude_directories=standard_exclude_directories,
    only_in_packages=True,
    show_ignored=False):
    """
    Return a dictionary suitable for use in ``package_data``
    in a distutils ``setup.py`` file.

    The dictionary looks like::

        {'package': [files]}

    Where ``files`` is a list of all the files in that package that
    don't match anything in ``exclude``.

    If ``only_in_packages`` is true, then top-level directories that
    are not packages won't be included (but directories under packages
    will).

    Directories matching any pattern in ``exclude_directories`` will
    be ignored; by default directories with leading ``.``, ``CVS``,
    and ``_darcs`` will be ignored.

    If ``show_ignored`` is true, then all the files that aren't
    included in package data are shown on stderr (for debugging
    purposes).

    Note patterns use wildcards, or can be exact paths (including
    leading ``./``), and all searching is case-insensitive.
    """

    out = {}
    stack = [(convert_path(where), '', package, only_in_packages)]
    while stack:
        where, prefix, package, only_in_packages = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print(
                                "Directory %s ignored by pattern %s" % (fn, pattern),
                                file=sys.stderr
                            )

                        break
                if bad_name:
                    continue
                if (os.path.isfile(os.path.join(fn, '__init__.py'))
                    and not prefix):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                    stack.append((fn, '', new_package, False))
                else:
                    stack.append((fn, prefix + name + '/', package, only_in_packages))
            elif package or not only_in_packages:
                # is a file
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        if show_ignored:
                            print(
                                "File %s ignored by pattern %s" % (fn, pattern),
                                file=sys.stderr
                                )
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out


def get_requirements():
    with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
        requirements_list = [req.strip() for req in f.readlines()]

    requirements_list.append("setuptools")
    requirements_list.append("pytz")
    return requirements_list


LONG_DESCRIPTION = """
===============
django-helpdesk
===============

This is a Django-powered helpdesk ticket tracker, designed to
plug into an existing Django website and provide you with
internal (or, perhaps, external) helpdesk management.
"""

setup(
    name='django-helpdesk',
    version=version,
    description="Django-powered ticket tracker for your helpdesk",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
        "Natural Language :: English",
    ],
    keywords=['django', 'helpdesk', 'django-helpdesk', 'tickets', 'incidents',
              'cases', 'bugs', 'track', 'support'],
    author='Ross Poulton',
    author_email='ross@rossp.org',
    maintainer='Garret Wassermann',
    maintainer_email='gwasser@gmail.com',
    url='https://github.com/django-helpdesk/django-helpdesk',
    license='BSD',
    packages=find_packages(),
    package_data=find_package_data("helpdesk", only_in_packages=False),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements(),
)

