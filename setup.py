from setuptools import setup

setup(
    name="pypapermerge",
    version="0.1",
    description="A papermerge api client",
    author="Philipp Rintz",
    author_email="git@rintz.net",
    packages=["pypapermerge", "pypapermerge.endpoints"],
    install_requires=["loguru", "requests", "python-decouple"],
    python_requires=">=3.8",
)
