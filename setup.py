from setuptools import setup, find_packages

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(name='pysportsref',
      version_format='0.0.1',
      packages=find_packages(),
      description='Utilities for working with Sports Reference',
      install_requires=['bs4', 'numpy', 'pandas', 'requests', 'lxml', 'tqdm'],
      long_description=long_description,
      license='MIT',
      url='https://github.com/hwchase17/pysportsref')
