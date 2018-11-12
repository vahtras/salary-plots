from setuptools import setup

setup(
    name="catplot",
    packages=["catplot"],
    install_requires=["pandas", "seaborn"],
    scripts=["scripts/boxplot", "scripts/pointplot"],
)
