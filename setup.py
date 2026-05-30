"""
DocuMind - Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

setup(
    name="documind",
    version="1.0.0",
    author="DocuMind Team",
    author_email="documind@example.com",
    description="Lightweight AI Document Intelligence Parser - 轻量级AI文档智能解析工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/documind",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Zero-dependency design - only standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "documind=documind.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="document parser markdown converter extractor analyzer text processing",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/documind/issues",
        "Source": "https://github.com/yourusername/documind",
        "Documentation": "https://github.com/yourusername/documind#readme",
    },
)
