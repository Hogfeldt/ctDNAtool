from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ctDNAtool",
    version="0.0.1",
    author="Per Høgfeldt",
    description="A software for creating and manipulating statistics from ctDNA data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hogfeldt/ctDNAtool",
    packages=find_packages("src"),
    package_dir={"": "src"},
    test_suite="test",
    install_requires=[
        "pysam",  # 0.15.4
        "numpy",  # 1.18.1
        "attrs",  # 19.3.0
        "click>=7.0",
        "py2bit",
        # "pandas", # 1.0.3
        # "matplotlib",   #3.2.1
        # "seaborn",      #0.10.1
        "scipy",  # 1.4.1
        "natsort",
    ],
    entry_points={
        "console_scripts": [
            "ctDNAtool = ctDNAtool.cli:cli",
            "ctDNAflow = ctDNAtool.cli_flow:cli_flow",
        ]
    },
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
