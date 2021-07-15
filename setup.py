import re
from os.path import dirname, join
from setuptools import find_packages, setup

with open(join(dirname(__file__), "url_downloader", "__init__.py")) as fp:
    for line in fp:
        m = re.search(r'^\s*__version__\s*=\s*([\'"])([^\'"]+)\1\s*$', line)
        if m:
            version = m.group(2)
            break
    else:
        raise RuntimeError("Unable to find own __version__ string")

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="url_downloader",
    version=version,
    author="Fabio Beranizo Lopes",
    author_email="fabio.beranizo@gmail.com",
    description="A didatic API that downloads the contents returned by url.",
    license="Apache",
    url="https://github.com/fberanizo/url_downloader",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.7.0",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
