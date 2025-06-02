"""Setup script for F1 Predictor package."""

from setuptools import find_packages, setup

# Read README file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="f1-predictor",
    version="1.0.0",
    author="Charles-François Fouti-Loemba",
    author_email="contact@f1predictor.com",
    description="Modèle de Machine Learning pour prédire les résultats des Grands Prix de Formule 1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/f1-predictor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.2.0",
        ],
        "all": [
            "mlflow>=2.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "f1-predictor=src.cli:main",
            "f1-train=scripts.train_model:main",
            "f1-collect=scripts.collect_data:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json"],
    },
) 