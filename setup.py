import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="Hammerhead-View",
  version="0.1.4",
  author="Xudong Liu",
  author_email="xudongliu98@gmail.com",
  description="A tool designed to de novo find potential modification sites.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/lrslab/Hammerhead",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  python_requires = '>=3.7, <=3.11',
  install_requires=[
  'termcolor >= 2.2.0',
  'pandas >= 2.0.3'
  ],
  scripts = ["Hammerhead_View/hammerhead",
      "Hammerhead_View/hammer_polish"]
)
