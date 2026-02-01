from setuptools import setup, find_packages

setup(
    name="nexus-cognitive-platform",
    version="0.1.0",
    description="AI-powered cognitive platform for understanding complex software systems",
    author="Soumyaatanna",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "networkx>=3.0",
        "matplotlib>=3.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nexus=nexus.cli:main",
        ],
    },
    python_requires=">=3.8",
)
