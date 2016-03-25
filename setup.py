# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path
import codecs


def readfile(file_path):
    return codecs.open(file_path, 'r', 'utf-8').read()


setup(
    name='python-myeventhub',
    version='0.1.1',

    author='Anton Kuzmichev',
    author_email='assargin@gmail.com',
    license='Apache Software License',

    packages=find_packages(exclude=("tests",)),
    requires=['six', ],
    install_requires=['six', ],

    description='Python API client for MyEventHub.ru',
    long_description=readfile(path.join(path.dirname(__file__), 'README.rst')),

    url='https://github.com/DirectlineDev/python-myeventhub',
    download_url='https://github.com/DirectlineDev/python-myeventhub/archive/master.zip',

    keywords=['python', 'myeventhub', 'myeventhub.ru', 'eventhub', 'myeventhub api', ],
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable', - coming soon
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
