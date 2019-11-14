from setuptools import setup, find_packages

setup(name='sportsref',
      version_format='0.0.1',
      packages=find_packages(),
      description='Utilities for working with Sports Reference',
      install_requires=['bs4', 'numpy', 'pandas', 'requests', 'lxml', 'tqdm'])
