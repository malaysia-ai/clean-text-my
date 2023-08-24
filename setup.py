from setuptools import setup, find_packages

__packagename__ = "clean_text_my"

with open("requirements.txt") as fopen:
    req = list(filter(None, fopen.read().split("\n")))


def readme():
    # TODO https://github.com/huseinzol05/malaya/blob/master/README-pypi.rst
    with open("README.md") as f:
        return f.read()


setup(
    name=__packagename__,
    description="",
    version="0.0.1",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=req,
    author="Malaysia AI",
    author_email="malaysia.ai2020@gmail.com",
    url="https://github.com/malaysia-ai/clean_text_my",
)
