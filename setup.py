from setuptools import setup, find_packages

requirements = []
with open("./requirements.txt", "r") as requirements_file:
  requirements = requirements_file.read().splitlines()

setup(
  name="poepyautopot",
  version="1.2.1",
  description="A Python based Autopot script for Path of Exile",
  url="http://github.com/passivelemon/poepyautopot/",
  author="PassiveLemon",
  author_email="jeremyseber@gmail.com",
  license="GPL3",
  packages=find_packages(),
  install_requires=requirements,
  entry_points={
    'console_scripts': [
      'poepyautopot = poepyautopot.__main__:main'
    ]
  },
  include_package_data=True,
)
