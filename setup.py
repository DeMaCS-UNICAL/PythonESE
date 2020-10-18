from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PythonESE",
    version="0.2.0",
    packages=find_packages(),
    scripts=['embasp_server_executor/embasp_server_executor.py'],

    install_requires=['embasp', 'tornado'],

    package_data={
        '': ['*.txt', '*.md'],
    },

    # test_suite
    # A string naming a unittest.TestCase subclass (or a package or module containing one or more of them, or a method of such a subclass), or naming a function that can be called with no arguments and returns a unittest.TestSuite. If the named suite is a module, and the module has an additional_tests() function, it is called and the results are added to the tests to be run. If the named suite is a package, any submodules and subpackages are recursively added to the overall test suite.
    # Specifying this argument enables use of the test command to run the specified test suite, e.g. via setup.py test. See the section on the test command below for more details.
    # tests_require
    # If your project’s tests need one or more additional packages besides those needed to install it, you can use this option to specify them. It should be a string or list of strings specifying what other distributions need to be present for the package’s tests to run. When you run the test command, setuptools will attempt to obtain these (even going so far as to download them using EasyInstall). Note that these required projects will not be installed on the system where the tests are run, but only downloaded to the project’s setup directory if they’re not already installed locally.

    # metadata to display on PyPI
    author="Stefano Germano",
    author_email="loide@mat.unical.it",
    description="Python web app to execute logic programs with different solvers, using the EmbASP framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="",
    url="https://github.com/DeMaCS-UNICAL/PythonESE",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/DeMaCS-UNICAL/PythonESE/issues",
        "Documentation": "",
        "Source Code": "https://github.com/DeMaCS-UNICAL/PythonESE",
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # could also include download_url, etc.
    
)
