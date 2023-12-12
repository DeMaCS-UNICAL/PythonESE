from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PythonESE",
    version="1.0.0",
    packages=find_packages(),
    scripts=['embasp_server_executor/ese_main.py'],

    install_requires=['embasp-python', 'tornado', 'antlr4-python3-runtime'],
    package_data={
        '': ['*.txt', '*.md'],
    },

    test_suite="tests",

    # metadata to display on PyPI
    author="Stefano Germano",
    author_email="loide@mat.unical.it",
    description="Python web-app to execute logic programs with different solvers, using the EmbASP framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="",
    url="https://github.com/DeMaCS-UNICAL/PythonESE",  # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/DeMaCS-UNICAL/PythonESE/issues",
        "Documentation": "",
        "Source Code": "https://github.com/DeMaCS-UNICAL/PythonESE",
    },
    download_url="https://github.com/DeMaCS-UNICAL/PythonESE/releases",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
