from setuptools import setup, find_packages

setup(
    name="pwa",
    packages=find_packages(),
    entry_points={
        "console_scripts" : [
            "pwa_except = pwa.scripts.check_except:main",
            "pwa_counts = pwa.scripts.counts:main",
            "pwa_purity = pwa.purity:purity_main",
            "pwa_graviton = pwa.graviton:graviton_main",
            "pwa_graviton_counts = pwa.graviton_counts:graviton_main",
            "pwa_shapes = pwa.showershapes:main",
            "pwa = pwa:main",
        ]
    }
)
