from setuptools import setup, find_packages  # type:ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name='gva.services',
   version='0.0.16',
   description='GVA Services',
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='joocer',
   author_email='justin.joyce@joocer.com',
   packages=find_packages(),
   url="https://github.com/gva-jhabte/gva_services",
   install_requires=['google-cloud-tasks', 'gva.data']
)