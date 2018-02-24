import os
from setuptools import setup

def path():
    return os.path.dirname(__file__)
    #return os.getcwd()



'''setup(
    name='TestDataGenerator',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0',

    description='A python project to create test data',
    long_description='A python project to create test data',

    # The project's main homepage.
    url='https://bitbucket.coke.com/projects/NSR/repos/testdatageneration/browse',

    # Author details
    author='Capgemini Americas Inc.',
    author_email='@capgemini.com',

    # Choose your license
    license='Capgemini Americas Inc',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers and Ops team',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: Approved :: Capgemini Americas Inc',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='sample test data generator',

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    scripts = ['src/main'],

)'''