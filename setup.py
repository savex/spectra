import glob
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()

DATA = [
    ('etc', [f for f in glob.glob(os.path.join('etc', '*'))]),
    ('templates', [f for f in glob.glob(os.path.join('templates', '*'))]),
    ('res', [f for f in glob.glob(os.path.join('res', '*'))])
]

dependencies = [
    'six',
    'jinja2'
]

entry_points = {
    "console_scripts":
        "inspector = spectra.inspector:inspector_cli_main"
}


setup(
    name="Spectra:Inspector",
    version="0.1.1",
    author="Alex Savatieiev",
    author_email="a.savex@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"
    ],
    keywords="QA, infrastructure, openstack, configuration, html, report",
    entry_points=entry_points,
    url="https://github.com/savex/spectra",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.conf', '*.list', '*.html']
    },
    zip_safe=False,
    install_requires=dependencies,
    data_files=DATA,
    license="Apache Licence, version 2",
    description="Spectra toolset used to gather, save and trend info "
                "in key config, process and file attribute points "
                "for a host or a list of remote hosts.",
    long_description=README
)

