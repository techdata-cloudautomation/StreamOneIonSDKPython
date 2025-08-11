from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='streamoneionsdk',
    version='0.1.3',
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
    long_description_content_type="text/markdown",  # or "text/x-rst" if using reStructuredText
)
