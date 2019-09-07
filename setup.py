import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="text-file-reader",
    version="1.0.0",
    author="Arin Khare",
    author_email="arinmkhare@gmail.com",
    description="Termial text file viewer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stcejorPmodnar/ph-hackathon-2019",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ],
    include_package_data=True,
)