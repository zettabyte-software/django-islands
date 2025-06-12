from os import path

from setuptools import find_packages, setup

# read the contents of your README file
this_directory = path.dirname(path.abspath(__file__))

with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()


# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="django-islands",
    version="0.0.2",  # Required
    description="Django Library to Implement Multi-Tenant Architecture via tenant_id column in Postgres",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yellow-devs/django-islands",
    author="Davi Silva Rafacho",
    author_email="davi.s.rafacho.developer@gmail.com",
    # Classifiers help users find your project by categorizing it.
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Database",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
    ],
    keywords=("django multi-tenant postgres saas"),
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "docs", "docs.*"]),
)
