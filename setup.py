from setuptools import setup

setup(
    name="catplot",
    packages=["catplot"],
    install_requires=["pandas", "seaborn", "xlrd"],
    scripts=[
        "scripts/boxplot",
        "scripts/boxplot-demo",
        "scripts/pointplot"
    ],
)
