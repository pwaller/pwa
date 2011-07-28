from setuptools import setup, find_packages

setup(
    name="egammaAnalysisUtils",
    packages=find_packages(),
    package_data={"egammaAnalysisUtils" :["*.C", "*.cxx", "egammaAnalysisUtils/*.h"]},
)
