from setuptools import setup, find_packages
from os.path import join, dirname
from yabuf import __version__

setup(
    name='yabuf',
    version=__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'yabuf = yabuf.main:main',
            ]
        },
    install_requires = [
        'Flask==0.10.1'
        ],
)
