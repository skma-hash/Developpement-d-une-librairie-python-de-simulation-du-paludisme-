from setuptools import setup, find_packages

setup(
    name="malaria-simulation",
    version="0.1.0",
    description="Malaria disease simulation library with Qt interface",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "matplotlib>=3.3.0",
        "PySide6>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "malaria-sim=main:main",
        ],
    },
)
