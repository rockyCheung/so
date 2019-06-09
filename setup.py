# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
import sys
import fcon

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported')

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open('LICENSE') as fp:
#     license = fp.read()

# os.system('export PYCURL_SSL_LIBRARY=openssl')

setup(
    name='sohot',
    version=fcon.__version__,
    description='高性能socketserver',
    long_description=long_description,
    # long_description_content_type="text/x-rst",
    long_description_content_type="text/markdown",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    author='Rocky',
    url='https://github.com/rockyCheung/so.git',
    author_email='274935730@qq.com',
    license='PSF',
    packages=find_packages(exclude=['contrib', 'docs', 'test']),
    install_requires=['wheel>=0.33.1','setuptools>=40.8.0','PyYAML>=3.13','pytest>=4.3.1','wrapt>=1.11.1','Click>=7.0','six>=1.12.0',
                      'celery>=4.3.0'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst','tmplate_conf.yml','*.md'],
        # And include any *.msg files found in the 'hello' package, too:
        'tip': ['*.msg'],
    },
#    include_package_data=False,
#     py_modules=["CurlClient", "ec_exception", "enums"],
    zip_safe=True,
    python_requires='>=3',
    scripts = [],
    entry_points = {
        'console_scripts': [
            'sohot = sohot.cli:start_so'
         ]
     }
)