from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    user_options = [
        ('token=', 'a', "JWT Token"),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.token = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main([
            "--token", self.token,
        ])
        sys.exit(errno)


if sys.version_info < (3, 6):
    raise RuntimeError("This package requres Python 3.6+")
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='LNMarkets',
    packages=find_packages(include=['LNMarkets']),
    version='1.4.0',
    description='LNMarkets API Wrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DivyanshuBagga/LNMarkets",
    author='Divyanshu Bagga',
    author_email="divyanshu.baggar@pm.me",
    license='MIT',
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    download_url='https://github.com/DivyanshuBagga/LNMarkets/archive/'
    '1.3.0.tar.gz',
    keywords=['Bitcoin', 'Finance', 'Trading'],
    python_requires='>=3.6',
    cmdclass={
        'test': PyTest,
    },
)
