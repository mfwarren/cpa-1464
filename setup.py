from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.1'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
]


setup(name='cpa-1464',
    version=version,
    description="Implementation of the Canadian Payment Association Standard 005,  1464 byte file format, for transmitting payments",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      'Development Status :: 3 - Alpha'
      'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.2',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4'
      'Intended Audience :: Financial and Insurance Industry',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Topic :: Office/Business :: Financial'
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='cpa 1464, standard 005, EFT, canadian payment association',
    author='Matt Warren',
    author_email='matt.warren@gmail.com',
    url='https://github.com/mfwarren/cpa-1464',
    license='MIT',
    packages=find_packages('src', exclude=['tests']),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires
)
