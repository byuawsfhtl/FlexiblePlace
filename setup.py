import setuptools
import os

version = {}
with open("_version.py", "r", encoding="utf-8") as fh:
    exec(fh.read(), version)
version = version["__version__"]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = ""
with open("FlexiblePlace/requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

requirements = [req for req in requirements.split("\n") if req.strip() and not req.strip().startswith("#")]

def list_folders(directory: str) -> list:
    """Creates a list of all the folders in a directory.

    Args:
        directory (str): the directory to search

    Returns:
        list: A list of all the folders in the directory
    """
    folders = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path) and item != "__pycache__":
            folders.append(item_path)
    other_folders = [list_folders(item_path) for item_path in folders]
    for folder in other_folders:
        folders.extend(folder)
    return folders

folder_path = "FlexiblePlace"
folders = list_folders(folder_path)
folders.append("FlexiblePlace")
folders = [os.path.normpath(folder).replace(os.sep, ".") for folder in folders]
print(folders)

setuptools.setup(
    name='FlexiblePlace',
    version=version,
    author='Record Linking Lab',
    author_email='recordlinkinglab@gmail.com',
    description='This is a library used to make fuzzy place comparisons.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/byuawsfhtl/FlexiblePlace.git',
    project_urls={
        "Bug Tracker": "https://github.com/byuawsfhtl/FlexiblePlace/issues"
    },
    packages=folders,
    install_requires=requirements,
    package_data={"": ["*.json", "*.txt"]},
)
