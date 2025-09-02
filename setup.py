from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='streamOneIonSDK',
    version='0.1.7',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            # Add command line scripts here
        ],
    },
    long_description=long_description,
    # or "text/x-rst" if using reStructuredText
    long_description_content_type="text/markdown",
)
