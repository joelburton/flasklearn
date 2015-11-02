from setuptools import setup, find_packages
setup(
    name='Flask-GZip',
    version='0.1',
    license='MIT',
    description='Flask extension to compress to GZip',
    author='Jack Stouffer',
    author_email='example@gmail.com',
    platforms='any',
    install_requires=['Flask'],
    packages=find_packages()
)