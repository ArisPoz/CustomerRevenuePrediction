from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='CustomerRevenuePrediction',
   version='1.0',
   description='Customer Revenue Prediction',
   license="GNU",
   long_description=long_description,
   author='Aristotelis Pozidis',
   packages=['CustomerRevenuePrediction'],
)
