from setuptools import setup

with open("./README.md") as fp:
     long_description = fp.read()

with open("./requirements.txt") as fp:
     dependencies = [line.strip() for line in fp.readlines()]


setup(name="OCR Computer Vision",
      version="0.1",
      description="OCR",
      long_desciption=long_description,
      author="Jean-Michel Cheumeni",
      author_email="cheumenijean@yahoo.fr",
      packages=["src"],
      install_requires=dependencies,
)