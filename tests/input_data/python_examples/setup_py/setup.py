from setuptools import find_packages, setup

setup(
    name="setup_py",
    version="0.0.1",
    author="Nick DeRobertis",
    author_email="derobertis.nick@gmail.com",
    description="[from setup.py] An example Python package for testing purposes (version from setup.py)",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
