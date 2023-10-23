from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()


setup(
    name='cex_arbitrage',
    version='1.0',
    packages=find_packages(exclude=['tests', 'docs']),
    # Automatically include all packages, excluding any test or documentation packages
    install_requires=read_requirements(),
    url='',
    license='MIT',
    author='Lucas Takara',
    author_email='lucastakara2@gmail.com',
    description='CEX Arbitrage POC'
)
