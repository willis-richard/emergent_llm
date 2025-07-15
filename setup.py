from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="evolutionary-llm",
    version="0.1.0",
    author="Richard Willis",
    author_email="richard.willis@kcl.ac.uk",
    description="Benchmarking emergent LLM behaviour in social dilemma games",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/willis-richard/emergent_llm",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "jupyter",
        "openai",
        "anthropic",
        "transformers",
        "pytest",
        "tqdm",
        "pyyaml",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "autoflake",
            "epc",
            "isort",
            "pandas-stubs",
            "ptvsd>=4.2",
            "pylsp-mypy",
            "python-lsp-server",  # though included by pylsp-mypy
        ],
    },
)
