'''
devops-tools: Devops Tools

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Copyright 2017, Pablo Venegas.
Licensed under MIT.
'''
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


version = "0.1"

setup(name="devops-tools",
      version=version,
      description="Devops Tools",
      long_description=open("README.rst").read(),
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Programming Language :: Python'
      ],
      keywords="devops docker", # Separate with spaces
      author="Pablo Venegas",
      author_email="pablo.venegas@gmail.com",
      url="",
      license="MIT",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      tests_require=['pytest'],
      cmdclass={'test': PyTest},

      # TODO: List of packages that this one depends upon:
      install_requires=['docker-py', 'dockerpty', 'PyYAML'],
      # TODO: List executable scripts, provided by the package (this is just an example)
      entry_points={
        'console_scripts':
            ['devops_tools=devopstools:main']
      }
)
