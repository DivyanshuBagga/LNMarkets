from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name='LNMarkets',
    packages=find_packages(include=['LNMarkets']),
    version='0.1.1',
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
    download_url = 'https://github.com/DivyanshuBagga/LNMarkets/archive/0.1.1.tar.gz',
    keywords = ['Bitcoin','Finance','Trading'],
)
