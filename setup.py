from distutils.core import setup
setup(
    name = "SSIS Datastore Syncer",
    packages = ['ssis_dss', 'cli'],
    version = "0.5",
    description = "Specialized Syncing software",
    author = "Adam Morris",
    author_email = "amorris@mistermorris.com",
    install_requires = ['click', 'sqlalchemy', 'psycopg2'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        ],
    entry_points='''
        [console_scripts]
        psmdlsyncer=cli.psmdlsyncer:psmdlsyncer
        ssisdss=cli.test:ssisdss_test
    ''',
    long_description = """\
TODO: DESCRIBE THIS!

This version requires Python 3 or later.
"""
)
