import setuptools
from shutil import rmtree

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="markdown2latex",
    version="1.0.0",
    description="CLI tool for converting Markdown with LaTeX to a .tex file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geajack/markdown2latex",
    py_modules=["markdown2latex"],
    classifiers=[
    ],
    python_requires='>=3.6',
    install_requires = [
        "marko"
    ],
    entry_points = {
        "console_scripts": [
            "markdown2latex=markdown2latex:main"
        ]
    }
)