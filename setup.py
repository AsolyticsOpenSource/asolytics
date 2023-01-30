from setuptools import setup, find_packages
from io import open
from os import path
import pathlib


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (not x.startswith('#')) and (not x.startswith('-'))]

dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]

setup (
 name = 'asolytics',
 description = 'ASO automation software tool on Google Play. Trend analysis, keyword popularity analysis and evaluation, competitor app analysis and keyword parsing.',
 version = '1.1.6',
 packages = find_packages(), # list of all packages
 install_requires = install_requires,
 python_requires='>=3.7', # any python greater than 2.7
 entry_points='''
        [console_scripts]
        asolytics=asolytics.asolytics:main
    ''',
 author="Asolytics Open Source",
 keywords="ASO tools, Google Play, app store optimization, ASO intelligence, app ranking, app market analysis, mobile apps marketing",
 long_description=README,
 long_description_content_type="text/markdown",
 license='MIT',
 url='https://github.com/AsolyticsOpenSource/asolytics',
 download_url='https://github.com/AsolyticsOpenSource/asolytics/archive/refs/tags/aso.zip',
  dependency_links=dependency_links,
  author_email='asolytics@gmail.com',
  classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)