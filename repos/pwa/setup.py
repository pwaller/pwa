from setuptools import setup, find_packages

setup(
    name="pwa",
    packages=find_packages(),
    install_requires=[
        #"minty",
        #"OQMaps",
        #"PhotonIDTool",
    ],
    entry_points={
        "console_scripts" : [
            "pwa_except = pwa.scripts.check_except:main",
            "pwa_counts = pwa.scripts.counts:main",
        ]
    }
)
