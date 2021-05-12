from setuptools import setup

setup(
    name="catplot",
    packages=["catplot"],
    install_requires=["pandas", "seaborn", "xlrd", "openpyxl, pyqt5"],
    scripts=[
        "scripts/boxplot",
        "scripts/boxplot-demo",
        "scripts/pointplot",
        "scripts/pointplot-demo",
        "scripts/stripplot",
        "scripts/stripplot-demo",
    ],
    entry_points={
        'console_scripts': ['catplot=catplot.main:main'],
    },
)
