from setuptools import setup, find_packages

setup(
    name='lab3',
    version='1.0.1',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = lab3.settings']},
)