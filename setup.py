from distutils.core import setup
from rd import __version__

long_description = open('README.rst').read()

setup(name="rd",
    version=str(__version__),
    py_modules=["rd"],
    description="Package for serializing and deserializing of XRD and JRD documents",
    author="Jeremy Carbaugh",
    author_email="jcarbaugh@gmail.com",
    license="BSD",
    url="http://github.com/jcarbaugh/python-rd/",
    long_description=long_description,
    install_requires=["isodate", "pytz", "requests"],
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
