"""
Document Parser Module
文档解析模块

Supports multiple document formats with intelligent content extraction.
支持多种文档格式，提供智能内容提取功能。
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum
import json


class DocumentType(Enum):
    """Supported document types"""
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MD = "markdown"
    HTML = "html"
    CSV = "csv"
    JSON = "json"
    XML = "xml"
    UNKNOWN = "unknown"


@dataclass
class DocumentSection:
    """Represents a section in a document"""
    title: str
    content: str
    level: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "content": self.content,
            "level": self.level,
            "metadata": self.metadata
        }


@dataclass
class ParsedDocument:
    """Represents a parsed document with structured content"""
    title: str = ""
    content: str = ""
    document_type: DocumentType = DocumentType.UNKNOWN
    sections: List[DocumentSection] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    tables: List[List[List[str]]] = field(default_factory=list)
    images: List[Dict[str, Any]] = field(default_factory=list)
    links: List[Dict[str, str]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "content": self.content,
            "document_type": self.document_type.value,
            "sections": [s.to_dict() for s in self.sections],
            "metadata": self.metadata,
            "tables": self.tables,
            "images": self.images,
            "links": self.links
        }
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class DocumentParser:
    """
    Main document parser class
    
    Features:
    - Multi-format document parsing (PDF, DOCX, TXT, MD, HTML, etc.)
    - Intelligent section detection and extraction
    - Table structure recognition
    - Link and image extraction
    - Metadata extraction
    """
    
    def __init__(self):
        self._parsers = {
            DocumentType.TXT: self._parse_txt,
            DocumentType.MD: self._parse_markdown,
            DocumentType.HTML: self._parse_html,
            DocumentType.JSON: self._parse_json,
            DocumentType.CSV: self._parse_csv,
            DocumentType.XML: self._parse_xml,
        }
    
    def detect_type(self, file_path: Union[str, Path]) -> DocumentType:
        """Detect document type from file extension"""
        ext = Path(file_path).suffix.lower()
        type_map = {
            '.pdf': DocumentType.PDF,
            '.docx': DocumentType.DOCX,
            '.txt': DocumentType.TXT,
            '.md': DocumentType.MD,
            '.markdown': DocumentType.MD,
            '.html': DocumentType.HTML,
            '.htm': DocumentType.HTML,
            '.csv': DocumentType.CSV,
            '.json': DocumentType.JSON,
            '.xml': DocumentType.XML,
        }
        return type_map.get(ext, DocumentType.UNKNOWN)
    
    def parse(self, file_path: Union[str, Path], **options) -> ParsedDocument:
        """
        Parse a document file
        
        Args:
            file_path: Path to the document file
            **options: Additional parsing options
            
        Returns:
            ParsedDocument object with structured content
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        doc_type = self.detect_type(file_path)
        
        if doc_type in self._parsers:
            return self._parsers[doc_type](file_path, **options)
        else:
            # Fallback to text parsing
            return self._parse_txt(file_path, **options)
    
    def parse_text(self, text: str, doc_type: DocumentType = DocumentType.TXT) -> ParsedDocument:
        """Parse text content directly"""
        parsed = ParsedDocument(
            content=text,
            document_type=doc_type
        )
        parsed.sections = self._extract_sections(text)
        parsed.links = self._extract_links(text)
        return parsed
    
    def _parse_txt(self, file_path: Path, **options) -> ParsedDocument:
        """Parse plain text files"""
        encoding = options.get('encoding', 'utf-8')
        
        try:
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()
        except Exception as e:
            raise IOError(f"Failed to read file: {e}")
        
        parsed = ParsedDocument(
            title=file_path.stem,
            content=content,
            document_type=DocumentType.TXT,
            metadata={
                "file_path": str(file_path),
                "file_size": os.path.getsize(file_path),
                "encoding": encoding
            }
        )
        
        # Extract sections based on headers
        parsed.sections = self._extract_sections(content)
        
        # Extract links
        parsed.links = self._extract_links(content)
        
        return parsed
    
    def _parse_markdown(self, file_path: Path, **options) -> ParsedDocument:
        """Parse Markdown files with structure extraction"""
        encoding = options.get('encoding', 'utf-8')
        
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()
        
        parsed = ParsedDocument(
            title=file_path.stem,
            content=content,
            document_type=DocumentType.MD,
            metadata={
                "file_path": str(file_path),
                "file_size": os.path.getsize(file_path)
            }
        )
        
        # Extract Markdown headers as sections
        parsed.sections = self._extract_markdown_sections(content)
        
        # Extract code blocks
        parsed.metadata["code_blocks"] = self._extract_code_blocks(content)
        
        # Extract links
        parsed.links = self._extract_markdown_links(content)
        
        return parsed
    
    def _parse_html(self, file_path: Path, **options) -> ParsedDocument:
        """Parse HTML files"""
        encoding = options.get('encoding', 'utf-8')
        
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()
        
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else file_path.stem
        
        # Remove script and style tags
        content_clean = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
        content_clean = re.sub(r'<style[^>]*>.*?</style>', '', content_clean, flags=re.IGNORECASE | re.DOTALL)
        
        # Extract text content (basic)
        text_content = re.sub(r'<[^>]+>', ' ', content_clean)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        parsed = ParsedDocument(
            title=title,
            content=text_content,
            document_type=DocumentType.HTML,
            metadata={
                "file_path": str(file_path),
                "html_tags": list(set(re.findall(r'<(\w+)', content)))
            }
        )
        
        # Extract links
        parsed.links = self._extract_html_links(content)
        
        return parsed
    
    def _parse_json(self, file_path: Path, **options) -> ParsedDocument:
        """Parse JSON files"""
        encoding = options.get('encoding', 'utf-8')
        
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()
        
        try:
            data = json.loads(content)
            formatted = json.dumps(data, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            data = None
            formatted = content
        
        parsed = ParsedDocument(
            title=file_path.stem,
            content=formatted,
            document_type=DocumentType.JSON,
            metadata={
                "file_path": str(file_path),
                "is_valid_json": data is not None,
                "keys": list(data.keys()) if isinstance(data, dict) else []
            }
        )
        
        return parsed
    
    def _parse_csv(self, file_path: Path, **options) -> ParsedDocument:
        """Parse CSV files"""
        encoding = options.get('encoding', 'utf-8')
        delimiter = options.get('delimiter', ',')
        
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            lines = f.readlines()
        
        tables = []
        for line in lines:
            row = line.strip().split(delimiter)
            if not tables:
                tables.append([row])
            else:
                tables[0].append(row)
        
        parsed = ParsedDocument(
            title=file_path.stem,
            content='\n'.join(lines),
            document_type=DocumentType.CSV,
            metadata={
                "file_path": str(file_path),
                "row_count": len(lines),
                "delimiter": delimiter
            },
            tables=tables
        )
        
        return parsed
    
    def _parse_xml(self, file_path: Path, **options) -> ParsedDocument:
        """Parse XML files"""
        encoding = options.get('encoding', 'utf-8')
        
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()
        
        # Extract root element
        root_match = re.search(r'<(\w+)[^>]*>', content)
        root_element = root_match.group(1) if root_match else "unknown"
        
        # Extract text content
        text_content = re.sub(r'<[^>]+>', ' ', content)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        parsed = ParsedDocument(
            title=file_path.stem,
            content=text_content,
            document_type=DocumentType.XML,
            metadata={
                "file_path": str(file_path),
                "root_element": root_element,
                "xml_tags": list(set(re.findall(r'<(\w+)', content)))
            }
        )
        
        return parsed
    
    def _extract_sections(self, content: str) -> List[DocumentSection]:
        """Extract sections based on header patterns"""
        sections = []
        
        # Pattern for headers like "# Header", "## Header", etc.
        header_pattern = r'^(#{1,6})\s+(.+)$'
        
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            match = re.match(header_pattern, line)
            if match:
                # Save previous section
                if current_section:
                    current_section.content = '\n'.join(current_content).strip()
                    sections.append(current_section)
                
                level = len(match.group(1))
                title = match.group(2).strip()
                current_section = DocumentSection(title=title, content="", level=level)
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # Save last section
        if current_section:
            current_section.content = '\n'.join(current_content).strip()
            sections.append(current_section)
        
        # If no sections found, create one from all content
        if not sections and content.strip():
            sections.append(DocumentSection(
                title="Content",
                content=content.strip(),
                level=1
            ))
        
        return sections
    
    def _extract_markdown_sections(self, content: str) -> List[DocumentSection]:
        """Extract sections from Markdown with special handling"""
        return self._extract_sections(content)
    
    def _extract_code_blocks(self, content: str) -> List[Dict[str, str]]:
        """Extract code blocks from Markdown"""
        code_blocks = []
        
        # Pattern for fenced code blocks
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for lang, code in matches:
            code_blocks.append({
                "language": lang or "text",
                "code": code.strip()
            })
        
        return code_blocks
    
    def _extract_links(self, content: str) -> List[Dict[str, str]]:
        """Extract URLs from text"""
        links = []
        url_pattern = r'https?://[^\s<>"\')\]]+'
        
        for url in re.findall(url_pattern, content):
            links.append({"url": url, "text": url})
        
        return links
    
    def _extract_markdown_links(self, content: str) -> List[Dict[str, str]]:
        """Extract Markdown-style links"""
        links = []
        
        # Pattern: [text](url)
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(pattern, content)
        
        for text, url in matches:
            links.append({"text": text, "url": url})
        
        # Also extract plain URLs
        links.extend(self._extract_links(content))
        
        return links
    
    def _extract_html_links(self, content: str) -> List[Dict[str, str]]:
        """Extract links from HTML"""
        links = []
        
        # Pattern: <a href="url">text</a>
        pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>'
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        
        for url, text in matches:
            # Remove HTML tags from text
            text = re.sub(r'<[^>]+>', '', text).strip()
            links.append({"text": text or url, "url": url})
        
        return links
