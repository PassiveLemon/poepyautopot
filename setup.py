from setuptools import setup, find_packages

requirements = [ ]
with open("./requirements.txt", "r") as requirements_file:
  requirements = requirements_file.read().splitlines()

setup(
  name = "poepyautopot",
  version = "1.3.6",
  description = "A Python based Autopot script for Path of Exile",
  url = "http://github.com/passivelemon/poepyautopot/",
  author = "PassiveLemon",
  license = "GPL3",
  packages = find_packages(),
  install_requires = requirements,
  entry_points={
    'console_scripts': [
      'poepyautopot = poepyautopot.__main__:main'
    ]
  },
  include_package_data = True,
)
