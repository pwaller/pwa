from setuptools import setup, find_packages

setup(
    name="EnergyRescalerTool",
    packages=find_packages(),
    package_data={"EnergyRescalerTool" :["*.C", "*.cxx", "*.h"]},
)
