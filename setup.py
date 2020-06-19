from setuptools import setup

setup(
    name="lesser",
    py_modules=["lesser"],
    version="0.0.1",
    install_requires=[
        "blobfile~=0.16",
        "flask~=1.1.2",
    ],
    description="Remote objects using rcall",
    author="OpenAI",
)
