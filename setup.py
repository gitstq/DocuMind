#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DocuMind Setup Script
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
    description="Lightweight Document Intelligence Processing Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/DocuMind",
    py_modules=["documind"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "documind=documind:main",
        ],
    },
    keywords="document processing, text analysis, knowledge extraction, pdf, markdown, nlp",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/DocuMind/issues",
        "Source": "https://github.com/gitstq/DocuMind",
    },
)
