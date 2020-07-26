import setuptools
from glob import glob
from os.path import basename
from os.path import splitext

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mabd",
    version="0.1",
    author="circius",
    author_email="circius@posteo.de",
    description="helper client for mutual-aid brighton airtable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[],
    python_requires=">=3.6",
    setup_requires=["pytest-runner",],
    install_requires=[
        "airtable-python-wrapper",
        "flask",
        "Flask-SQLAlchemy",
        "flask-login",
        "flask-migrate",
        "flask-security",
    ],
    entry_points="""""",
)
