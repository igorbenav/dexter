import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='dexter',
    version='0.0.7',
    description='Data Exploration Terser',
    long_description=README,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Operating System :: OS Independent',
        'Framework :: IPython',
      ],
    long_description_content_type='text/markdown',
    url="https://github.com/igormagalhaesr/dexter",
    author='Igor Magalhaes',
    author_email='igor.magalhaes.r@gmail.com',
    license='BSD 3',
    packages=find_packages(exclude=("tests",)),
    keyworks='Dataframes',
    project_urls={
        'Documentation': 'https://github.com/igormagalhaesr/dexter/blob/main/README.md',
        'Source': 'https://github.com/igormagalhaesr/dexter',
        'Tracker': 'https://github.com/igormagalhaesr/dexter/issues',
    },
)
