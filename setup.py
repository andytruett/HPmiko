import setuptools

with open("README.rst", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="HPmiko",
    version="1.1.0",
    author="Andy Truett",
    author_email="andrew.truett@gmail.com",
    description="HPmiko is a middle-man script to simplify extracting data from HP/Aruba Procurve switches using Netmiko",
    long_description_content_type="text/x-rst",
    long_description=long_description,
    license="MIT License",
    keywords="HP Aruba Procurve netmiko",
    url="https://github.com/andytruett/HPmiko",
    download_url="https://github.com/andytruett/HPmiko/archive/1.0.0.tar.gz",
    packages=setuptools.find_packages(),
    install_requires=["netmiko>=2.4.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
