"""
DocuMind - Lightweight AI Document Intelligence Parser
轻量级AI文档智能解析工具

A zero-dependency, local-first document parsing and structured data extraction tool.
零依赖、本地优先的文档解析与结构化数据提取工具。
"""

__version__ = "1.0.0"
__author__ = "DocuMind Team"
__license__ = "MIT"

from .parser import DocumentParser
from .extractor import StructuredExtractor
from .converter import MarkdownConverter
from .analyzer import DocumentAnalyzer

__all__ = [
    "DocumentParser",
    "StructuredExtractor", 
    "MarkdownConverter",
    "DocumentAnalyzer",
]
