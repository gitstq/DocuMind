#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DocuMind - Lightweight Document Intelligence Processing Engine
轻量级文档智能处理引擎

A zero-dependency Python tool for intelligent document processing,
knowledge extraction, and content analysis.

Author: DocuMind Team
License: MIT
Version: 1.0.0
"""

import os
import sys
import re
import json
import math
import argparse
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Set
from collections import Counter
from datetime import datetime
import io

__version__ = "1.0.0"
__author__ = "DocuMind Team"


class Colors:
    """Terminal color codes"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'


class TextUtils:
    """Text processing utilities"""

    STOP_WORDS = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
        'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
        'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'between', 'under', 'and', 'but', 'or', 'yet', 'so', 'if',
        'because', 'although', 'though', 'while', 'where', 'when', 'that',
        'which', 'who', 'whom', 'whose', 'what', 'this', 'these', 'those',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
        'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'mine',
        'yours', 'hers', 'ours', 'theirs', 'myself', 'yourself', 'himself',
        'herself', 'itself', 'ourselves', 'yourselves', 'themselves'
    }

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Tokenize text into words"""
        text = text.lower()
        words = re.findall(r'\b[a-z]+\b', text)
        return [w for w in words if len(w) > 2 and w not in TextUtils.STOP_WORDS]

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace in text"""
        return ' '.join(text.split())

    @staticmethod
    def extract_sentences(text: str) -> List[str]:
        """Extract sentences from text"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def calculate_tf_idf(documents: List[str]) -> Dict[str, float]:
        """Calculate TF-IDF scores for terms across documents"""
        if not documents:
            return {}

        # Tokenize all documents
        doc_tokens = [TextUtils.tokenize(doc) for doc in documents]
        all_terms = set()
        for tokens in doc_tokens:
            all_terms.update(tokens)

        # Calculate IDF
        idf = {}
        n_docs = len(documents)
        for term in all_terms:
            doc_count = sum(1 for tokens in doc_tokens if term in tokens)
            idf[term] = math.log(n_docs / (doc_count + 1)) + 1

        # Calculate TF-IDF for first document (main document)
        if doc_tokens:
            tokens = doc_tokens[0]
            tf = Counter(tokens)
            total_terms = len(tokens)
            tf_idf = {}
            for term, count in tf.items():
                tf_score = count / total_terms
                tf_idf[term] = tf_score * idf.get(term, 1)
            return tf_idf

        return {}


class PDFParser:
    """Simple PDF text parser (zero external dependencies)"""

    @staticmethod
    def parse(file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            # Extract text from PDF content
            text = PDFParser._extract_text_from_pdf(content)
            return text
        except Exception as e:
            return f"Error parsing PDF: {str(e)}"

    @staticmethod
    def _extract_text_from_pdf(content: bytes) -> str:
        """Extract text from PDF binary content"""
        text_parts = []

        # Find all text objects in PDF
        # Look for BT (Begin Text) and ET (End Text) markers
        pattern = rb'BT\s*(.*?)\s*ET'
        matches = re.findall(pattern, content, re.DOTALL)

        for match in matches:
            try:
                # Extract text from Tj and TJ operators
                text = PDFParser._decode_pdf_text(match)
                if text:
                    text_parts.append(text)
            except:
                pass

        # Also try to extract from stream objects
        stream_pattern = rb'stream\s*(.*?)\s*endstream'
        streams = re.findall(stream_pattern, content, re.DOTALL)

        for stream in streams:
            try:
                # Try to decode flate-encoded streams
                decoded = PDFParser._try_decode_stream(stream)
                if decoded:
                    text = PDFParser._extract_text_from_stream(decoded)
                    if text:
                        text_parts.append(text)
            except:
                pass

        # Fallback: extract any readable text
        if not text_parts:
            text = PDFParser._extract_readable_text(content)
            if text:
                return text

        return '\n'.join(text_parts)

    @staticmethod
    def _decode_pdf_text(data: bytes) -> str:
        """Decode text from PDF content"""
        text = ''
        # Look for Tj operator (text show)
        tj_pattern = rb'\((.*?)\)\s*Tj'
        tj_matches = re.findall(tj_pattern, data)
        for m in tj_matches:
            try:
                text += m.decode('utf-8', errors='ignore') + ' '
            except:
                pass

        # Look for TJ operator (text show with array)
        tj_array_pattern = rb'\[(.*?)\]\s*TJ'
        tj_array_matches = re.findall(tj_array_pattern, data)
        for m in tj_array_matches:
            try:
                # Extract strings from array
                strings = re.findall(rb'\((.*?)\)', m)
                for s in strings:
                    text += s.decode('utf-8', errors='ignore')
                text += ' '
            except:
                pass

        return text

    @staticmethod
    def _try_decode_stream(data: bytes) -> Optional[bytes]:
        """Try to decompress PDF stream"""
        try:
            # Check for FlateDecode
            if b'FlateDecode' in data[:100]:
                import zlib
                # Remove any filter parameters
                start = data.find(b'\x78\x9c')  # zlib header
                if start != -1:
                    return zlib.decompress(data[start:])
        except:
            pass
        return data

    @staticmethod
    def _extract_text_from_stream(data: bytes) -> str:
        """Extract text from decoded stream"""
        text = ''
        # Look for text operators
        pattern = rb'\(([^)]+)\)'
        matches = re.findall(pattern, data)
        for m in matches:
            try:
                decoded = m.decode('utf-8', errors='ignore')
                if len(decoded) > 1 and not decoded.startswith('/'):
                    text += decoded + ' '
            except:
                pass
        return text

    @staticmethod
    def _extract_readable_text(content: bytes) -> str:
        """Extract any readable ASCII/UTF-8 text from PDF"""
        text_parts = []
        # Find sequences of printable characters
        pattern = rb'[\x20-\x7E]{4,}'
        matches = re.findall(pattern, content)
        for m in matches:
            try:
                text = m.decode('utf-8', errors='ignore')
                # Filter out common PDF keywords
                if not any(kw in text for kw in ['/Type', '/Font', '/Width', '/Height', '/MediaBox']):
                    text_parts.append(text)
            except:
                pass
        return ' '.join(text_parts)


class MarkdownParser:
    """Markdown document parser"""

    @staticmethod
    def parse(file_path: str) -> Dict[str, Any]:
        """Parse markdown file and extract structure"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        return MarkdownParser._parse_content(content)

    @staticmethod
    def _parse_content(content: str) -> Dict[str, Any]:
        """Parse markdown content"""
        result = {
            'title': '',
            'headings': [],
            'paragraphs': [],
            'code_blocks': [],
            'links': [],
            'lists': [],
            'tables': []
        }

        lines = content.split('\n')
        i = 0
        current_code_block = None
        current_list = []
        in_list = False

        while i < len(lines):
            line = lines[i]

            # Extract title (first H1)
            if not result['title']:
                title_match = re.match(r'^#\s+(.+)$', line)
                if title_match:
                    result['title'] = title_match.group(1).strip()

            # Extract headings
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                result['headings'].append({'level': level, 'text': text})

            # Code blocks
            if line.strip().startswith('```'):
                if current_code_block is None:
                    lang = line.strip()[3:].strip()
                    current_code_block = {'language': lang, 'content': []}
                else:
                    current_code_block['content'] = '\n'.join(current_code_block['content'])
                    result['code_blocks'].append(current_code_block)
                    current_code_block = None
                i += 1
                continue

            if current_code_block is not None:
                current_code_block['content'].append(line)
                i += 1
                continue

            # Lists
            list_match = re.match(r'^[\s]*[-*+]\s+(.+)$', line)
            if list_match:
                if not in_list:
                    in_list = True
                    current_list = []
                current_list.append(list_match.group(1).strip())
            elif in_list and line.strip():
                # Continue list item
                current_list[-1] += ' ' + line.strip()
            elif in_list:
                result['lists'].append(current_list)
                current_list = []
                in_list = False

            # Tables
            if '|' in line and not line.strip().startswith('>'):
                table_match = re.match(r'^[\s]*\|(.+)\|[\s]*$', line)
                if table_match and not re.match(r'^[\s|\-:]+$', line.strip()):
                    cells = [cell.strip() for cell in table_match.group(1).split('|')]
                    if cells:
                        result['tables'].append(cells)

            # Links
            link_matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', line)
            for text, url in link_matches:
                result['links'].append({'text': text, 'url': url})

            # Paragraphs (non-empty lines that aren't special)
            if line.strip() and not any([
                line.strip().startswith('#'),
                line.strip().startswith('-'),
                line.strip().startswith('*'),
                line.strip().startswith('>'),
                line.strip().startswith('```'),
                line.strip().startswith('|'),
                '[' in line and '](' in line
            ]):
                result['paragraphs'].append(line.strip())

            i += 1

        # Handle remaining list
        if current_list:
            result['lists'].append(current_list)

        return result


class TextParser:
    """Plain text document parser"""

    @staticmethod
    def parse(file_path: str) -> Dict[str, Any]:
        """Parse plain text file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        lines = content.split('\n')

        return {
            'title': lines[0][:100] if lines else '',
            'paragraphs': [line.strip() for line in lines if line.strip()],
            'content': content
        }


class DocxParser:
    """DOCX file parser (zero dependencies)"""

    @staticmethod
    def parse(file_path: str) -> Dict[str, Any]:
        """Parse DOCX file and extract text"""
        try:
            with zipfile.ZipFile(file_path, 'r') as z:
                # Read document.xml
                xml_content = z.read('word/document.xml').decode('utf-8')

                # Extract text from XML
                text = DocxParser._extract_text_from_xml(xml_content)

                return {
                    'title': '',
                    'paragraphs': [p for p in text.split('\n') if p.strip()],
                    'content': text
                }
        except Exception as e:
            return {
                'title': '',
                'paragraphs': [],
                'content': f"Error parsing DOCX: {str(e)}"
            }

    @staticmethod
    def _extract_text_from_xml(xml: str) -> str:
        """Extract text from DOCX XML"""
        # Remove XML tags and extract text content
        text_parts = []

        # Find all w:t elements (text elements in Word)
        pattern = r'<w:t[^>]*>([^<]*)</w:t>'
        matches = re.findall(pattern, xml)

        for match in matches:
            if match:
                text_parts.append(match)

        # Join with spaces, but add newlines for paragraph breaks
        result = []
        for part in text_parts:
            result.append(part)

        return ' '.join(result)


class DocumentSummarizer:
    """Document summarization engine"""

    @staticmethod
    def summarize(text: str, ratio: float = 0.2) -> str:
        """Generate extractive summary of text"""
        sentences = TextUtils.extract_sentences(text)

        if len(sentences) <= 3:
            return text

        # Calculate sentence scores based on word frequency
        word_freq = TextUtils.calculate_tf_idf([text])

        sentence_scores = []
        for sentence in sentences:
            words = TextUtils.tokenize(sentence)
            score = sum(word_freq.get(word, 0) for word in words)
            if words:
                score /= len(words)
            sentence_scores.append((sentence, score))

        # Sort by score and select top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        num_sentences = max(1, int(len(sentences) * ratio))
        top_sentences = [s[0] for s in sentence_scores[:num_sentences]]

        # Restore original order
        summary_sentences = [s for s in sentences if s in top_sentences]

        return ' '.join(summary_sentences)


class KeywordExtractor:
    """Keyword extraction engine"""

    @staticmethod
    def extract(text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """Extract top keywords from text"""
        tf_idf = TextUtils.calculate_tf_idf([text])

        # Sort by score
        sorted_keywords = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)

        return sorted_keywords[:top_n]


class KnowledgeGraph:
    """Simple knowledge graph builder"""

    def __init__(self):
        self.entities: Set[str] = set()
        self.relations: List[Dict[str, str]] = []

    def extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text (simple approach)"""
        entities = []

        # Extract capitalized phrases (potential proper nouns)
        pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        matches = re.findall(pattern, text)
        entities.extend(matches)

        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        entities.extend(emails)

        # Extract URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text)
        entities.extend(urls)

        return list(set(entities))

    def build(self, text: str) -> Dict[str, Any]:
        """Build knowledge graph from text"""
        self.entities = set(self.extract_entities(text))

        # Extract simple relations (entity near entity)
        sentences = TextUtils.extract_sentences(text)
        for sentence in sentences:
            sent_entities = [e for e in self.entities if e in sentence]
            if len(sent_entities) >= 2:
                for i in range(len(sent_entities) - 1):
                    self.relations.append({
                        'source': sent_entities[i],
                        'target': sent_entities[i + 1],
                        'context': sentence[:100]
                    })

        return {
            'entities': list(self.entities),
            'relations': self.relations
        }

    def to_mermaid(self) -> str:
        """Export knowledge graph as Mermaid diagram"""
        lines = ['graph TD']

        # Add entities as nodes
        for i, entity in enumerate(self.entities):
            safe_entity = re.sub(r'[^\w]', '_', entity[:30])
            lines.append(f'    {safe_entity}["{entity[:50]}"]')

        # Add relations as edges
        for rel in self.relations[:20]:  # Limit to avoid too complex diagram
            source = re.sub(r'[^\w]', '_', rel['source'][:30])
            target = re.sub(r'[^\w]', '_', rel['target'][:30])
            lines.append(f'    {source} --> {target}')

        return '\n'.join(lines)


class DocumentProcessor:
    """Main document processing engine"""

    SUPPORTED_FORMATS = {
        '.txt': TextParser,
        '.md': MarkdownParser,
        '.markdown': MarkdownParser,
        '.pdf': PDFParser,
        '.docx': DocxParser
    }

    def __init__(self):
        self.stats = {
            'processed': 0,
            'failed': 0,
            'total_words': 0
        }

    def process_file(self, file_path: str, options: Dict[str, bool] = None) -> Dict[str, Any]:
        """Process a single document file"""
        options = options or {}
        result = {
            'file': file_path,
            'format': '',
            'success': False,
            'content': '',
            'metadata': {},
            'summary': '',
            'keywords': [],
            'knowledge_graph': None
        }

        ext = Path(file_path).suffix.lower()
        result['format'] = ext

        try:
            if ext not in self.SUPPORTED_FORMATS:
                result['error'] = f"Unsupported format: {ext}"
                self.stats['failed'] += 1
                return result

            parser = self.SUPPORTED_FORMATS[ext]

            if ext == '.pdf':
                content = parser.parse(file_path)
                parsed = {
                    'title': Path(file_path).stem,
                    'paragraphs': content.split('\n'),
                    'content': content
                }
            elif ext == '.docx':
                parsed = parser.parse(file_path)
                content = parsed.get('content', '')
            elif ext in ['.md', '.markdown']:
                parsed = parser.parse(file_path)
                content = '\n'.join(parsed.get('paragraphs', []))
            else:
                parsed = parser.parse(file_path)
                content = parsed.get('content', '')

            result['content'] = content
            result['metadata'] = {
                'title': parsed.get('title', Path(file_path).stem),
                'paragraphs': len(parsed.get('paragraphs', [])),
                'word_count': len(content.split()),
                'char_count': len(content)
            }

            self.stats['total_words'] += result['metadata']['word_count']

            # Generate summary
            if options.get('summarize', True) and len(content) > 200:
                result['summary'] = DocumentSummarizer.summarize(content)

            # Extract keywords
            if options.get('keywords', True):
                result['keywords'] = KeywordExtractor.extract(content, top_n=15)

            # Build knowledge graph
            if options.get('knowledge_graph', False):
                kg = KnowledgeGraph()
                result['knowledge_graph'] = kg.build(content)
                result['knowledge_graph_mermaid'] = kg.to_mermaid()

            result['success'] = True
            self.stats['processed'] += 1

        except Exception as e:
            result['error'] = str(e)
            self.stats['failed'] += 1

        return result

    def process_directory(self, dir_path: str, recursive: bool = True,
                          options: Dict[str, bool] = None) -> List[Dict[str, Any]]:
        """Process all documents in a directory"""
        results = []
        path = Path(dir_path)

        pattern = '**/*' if recursive else '*'
        for file_path in path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                result = self.process_file(str(file_path), options)
                results.append(result)

        return results


class TUI:
    """Terminal User Interface"""

    def __init__(self):
        self.colors = Colors()
        self.use_colors = sys.stdout.isatty()

    def _color(self, color: str, text: str) -> str:
        """Apply color to text if terminal supports it"""
        if self.use_colors:
            return f"{color}{text}{self.colors.RESET}"
        return text

    def print_header(self, title: str):
        """Print formatted header"""
        width = 60
        print()
        print(self._color(self.colors.CYAN, '═' * width))
        print(self._color(self.colors.BOLD + self.colors.CYAN, f'  {title}'))
        print(self._color(self.colors.CYAN, '═' * width))
        print()

    def print_section(self, title: str):
        """Print section header"""
        print()
        print(self._color(self.colors.YELLOW, f'▸ {title}'))
        print(self._color(self.colors.DIM, '─' * 50))

    def print_success(self, message: str):
        """Print success message"""
        print(self._color(self.colors.GREEN, f'✓ {message}'))

    def print_error(self, message: str):
        """Print error message"""
        print(self._color(self.colors.RED, f'✗ {message}'))

    def print_info(self, message: str):
        """Print info message"""
        print(self._color(self.colors.BLUE, f'ℹ {message}'))

    def print_stat(self, label: str, value: str):
        """Print statistic"""
        print(f"  {self._color(self.colors.DIM, label)}: {self._color(self.colors.WHITE, value)}")

    def print_progress(self, current: int, total: int, filename: str):
        """Print progress bar"""
        width = 40
        percent = current / total if total > 0 else 0
        filled = int(width * percent)
        bar = '█' * filled + '░' * (width - filled)
        print(f"\r  {bar} {percent*100:5.1f}% | {filename[:30]:30}", end='', flush=True)
        if current == total:
            print()


class DocuMindApp:
    """Main DocuMind application"""

    def __init__(self):
        self.processor = DocumentProcessor()
        self.tui = TUI()

    def run_cli(self):
        """Run command-line interface"""
        parser = argparse.ArgumentParser(
            description='DocuMind - Lightweight Document Intelligence Processing Engine',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
Examples:
  %(prog)s document.pdf                    # Process single file
  %(prog)s ./documents --recursive         # Process directory recursively
  %(prog)s file.md --summary --keywords    # Extract summary and keywords
  %(prog)s file.txt --knowledge-graph      # Build knowledge graph
  %(prog)s docs/ --output result.json      # Export to JSON
            '''
        )

        parser.add_argument('input', help='Input file or directory')
        parser.add_argument('-r', '--recursive', action='store_true',
                           help='Process directories recursively')
        parser.add_argument('-o', '--output', help='Output file (JSON format)')
        parser.add_argument('--no-summary', action='store_true',
                           help='Skip summary generation')
        parser.add_argument('--no-keywords', action='store_true',
                           help='Skip keyword extraction')
        parser.add_argument('-k', '--knowledge-graph', action='store_true',
                           help='Build knowledge graph')
        parser.add_argument('-v', '--version', action='version',
                           version=f'DocuMind {__version__}')

        args = parser.parse_args()

        # Show header
        self.tui.print_header(f'DocuMind v{__version__}')

        # Prepare options
        options = {
            'summarize': not args.no_summary,
            'keywords': not args.no_keywords,
            'knowledge_graph': args.knowledge_graph
        }

        # Process input
        input_path = Path(args.input)

        if not input_path.exists():
            self.tui.print_error(f"Path not found: {args.input}")
            sys.exit(1)

        results = []

        if input_path.is_file():
            self.tui.print_info(f"Processing file: {args.input}")
            result = self.processor.process_file(args.input, options)
            results.append(result)
            self._display_result(result)

        elif input_path.is_dir():
            self.tui.print_info(f"Processing directory: {args.input}")
            results = self.processor.process_directory(args.input, args.recursive, options)

            for i, result in enumerate(results, 1):
                self.tui.print_progress(i, len(results), Path(result['file']).name)
                if result['success']:
                    self.tui.print_success(f"Processed: {result['file']}")
                else:
                    self.tui.print_error(f"Failed: {result['file']} - {result.get('error', 'Unknown error')}")

        # Display statistics
        self._display_stats()

        # Export results
        if args.output:
            self._export_results(results, args.output)

        # Interactive summary display for single file
        if len(results) == 1 and results[0]['success']:
            self._display_detailed_result(results[0])

    def _display_result(self, result: Dict[str, Any]):
        """Display processing result"""
        if not result['success']:
            self.tui.print_error(f"Failed to process: {result.get('error', 'Unknown error')}")
            return

        self.tui.print_section('Document Metadata')
        meta = result['metadata']
        self.tui.print_stat('Title', meta.get('title', 'N/A'))
        self.tui.print_stat('Format', result['format'].upper())
        self.tui.print_stat('Words', str(meta.get('word_count', 0)))
        self.tui.print_stat('Characters', str(meta.get('char_count', 0)))
        self.tui.print_stat('Paragraphs', str(meta.get('paragraphs', 0)))

    def _display_detailed_result(self, result: Dict[str, Any]):
        """Display detailed processing result"""
        if result.get('summary'):
            self.tui.print_section('Document Summary')
            print(f"  {result['summary'][:500]}...")

        if result.get('keywords'):
            self.tui.print_section('Top Keywords')
            keywords_str = ', '.join([f"{kw[0]}({kw[1]:.2f})" for kw in result['keywords'][:10]])
            print(f"  {keywords_str}")

        if result.get('knowledge_graph_mermaid'):
            self.tui.print_section('Knowledge Graph (Mermaid)')
            print(result['knowledge_graph_mermaid'])

    def _display_stats(self):
        """Display processing statistics"""
        self.tui.print_section('Processing Statistics')
        stats = self.processor.stats
        self.tui.print_stat('Files Processed', str(stats['processed']))
        self.tui.print_stat('Files Failed', str(stats['failed']))
        self.tui.print_stat('Total Words', str(stats['total_words']))

    def _export_results(self, results: List[Dict[str, Any]], output_path: str):
        """Export results to JSON file"""
        try:
            # Clean results for JSON serialization
            clean_results = []
            for r in results:
                clean_r = {
                    'file': r.get('file', ''),
                    'format': r.get('format', ''),
                    'success': r.get('success', False),
                    'metadata': r.get('metadata', {}),
                    'summary': r.get('summary', ''),
                    'keywords': r.get('keywords', []),
                    'error': r.get('error', '')
                }
                if r.get('knowledge_graph'):
                    clean_r['knowledge_graph'] = r['knowledge_graph']
                clean_results.append(clean_r)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'export_time': datetime.now().isoformat(),
                    'documind_version': __version__,
                    'statistics': self.processor.stats,
                    'results': clean_results
                }, f, indent=2, ensure_ascii=False)

            self.tui.print_success(f"Results exported to: {output_path}")
        except Exception as e:
            self.tui.print_error(f"Failed to export: {str(e)}")


def main():
    """Main entry point"""
    app = DocuMindApp()
    app.run_cli()


if __name__ == '__main__':
    main()
