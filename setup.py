from setuptools import setup, find_packages

setup(
    name="smartpay-sdk",
    version="0.0.1",
    description="Smartpay SDK Python",
    url="https://github.com/smartpay-co/sdk-python",
    author="Smartpay Solutions PTE. LTD.",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["smartpay"],
    package_data={'': ['*.json']},
    install_requires=["requests"],
)
