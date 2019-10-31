import io
import sys

from setuptools import find_packages, setup

with open('calysto_processing/__init__.py', encoding='utf-8') as fid:
    for line in fid:
        if line.startswith('__version__'):
            __version__ = line.strip().split()[-1][1:-1]
            break

with open('README.md') as f:
    readme = f.read()

setup(name='calysto_processing',
      version=__version__,
      description='A ProcessingJS kernel for Jupyter',
      long_description=readme,
      url="https://github.com/Calysto/calysto_processing",
      author='Douglas Blank',
      author_email='doug.blank@gmail.com',
      install_requires=["metakernel", "html2text"],
      packages=find_packages(include=["calysto_processing", "calysto_processing.*"]),
      package_data={'calysto_processing': ["images/*.png", "modules/*.ss"]},
      classifiers = [
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 2',
          'Topic :: System :: Shells',
      ]
)
