from setuptools import setup, find_packages

setup(
    name='StreamOneIONSDK',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            # Add command line scripts here
        ],
    },
)
