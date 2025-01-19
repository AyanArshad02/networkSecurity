"""
This setup.py is an essential part of packaging and distribuitng python projects.
It is used by setuptools (or distutils in older python versions) to define the
configuration of your project, such as its metadata, dependencies, and more.
"""

from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    This function will return list of requirements
    """
    requirement_list = []
    try:
        with open('requirements.txt','r') as file:
            # Reading lines from file
            lines = file.readlines()
            # Processing each line
            for line in lines:
                requirement = line.strip()
                # Ignoring empty lines and -e.
                if requirement and requirement!= '-e.':
                    requirement_list.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_list


# print(get_requirements()) 

setup(
    name="Network Security",
    version="0.0.1",
    author="Md Ayan Arshad",
    email="ayanarshad2002@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)

