"""
Markdown Converter Module
Markdown转换模块

Converts various document formats to clean, structured Markdown.
将各种文档格式转换为干净、结构化的Markdown。
"""

import re
from pathlib import Path
from typing import Union, Optional, Dict, Any, List
from .parser import DocumentParser, ParsedDocument, DocumentType


class MarkdownConverter:
    """
    Document to Markdown converter
    
    Features:
    - Convert multiple formats to clean Markdown
    - Preserve document structure (headers, lists, tables)
    - Extract and format code blocks
    - Handle images and links appropriately
    - Support custom formatting options
    """
    
    def __init__(self):
        self.parser = DocumentParser()
    
    def convert(self, file_path: Union[str, Path], **options) -> str:
        """
        Convert a document to Markdown
        
        Args:
            file_path: Path to the document
            **options: Conversion options
                - include_metadata: Include YAML frontmatter (default: False)
                - include_toc: Include table of contents (default: False)
                - preserve_tables: Preserve table structure (default: True)
                - image_alt_text: Default alt text for images (default: "image")
                
        Returns:
            Markdown formatted string
        """
        file_path = Path(file_path)
        
        # Parse the document
        parsed = self.parser.parse(file_path)
        
        # Convert to Markdown
        return self._to_markdown(parsed, **options)
    
    def convert_text(self, text: str, doc_type: DocumentType = DocumentType.TXT, **options) -> str:
        """Convert text content to Markdown"""
        parsed = self.parser.parse_text(text, doc_type)
        return self._to_markdown(parsed, **options)
    
    def _to_markdown(self, parsed: ParsedDocument, **options) -> str:
        """Convert parsed document to Markdown"""
        include_metadata = options.get('include_metadata', False)
        include_toc = options.get('include_toc', False)
        
        lines = []
        
        # Add YAML frontmatter if requested
        if include_metadata and parsed.metadata:
            lines.append("---")
            for key, value in parsed.metadata.items():
                if isinstance(value, (list, dict)):
                    lines.append(f"{key}: {str(value)}")
                else:
                    lines.append(f"{key}: {value}")
            lines.append("---")
            lines.append("")
        
        # Add title
        if parsed.title:
            lines.append(f"# {parsed.title}")
            lines.append("")
        
        # Add table of contents if requested
        if include_toc and parsed.sections:
            lines.append("## Table of Contents")
            lines.append("")
            for section in parsed.sections:
                indent = "  " * (section.level - 1)
                anchor = self._to_anchor(section.title)
                lines.append(f"{indent}- [{section.title}](#{anchor})")
            lines.append("")
        
        # Add content sections
        if parsed.sections:
            for section in parsed.sections:
                header_prefix = "#" * min(section.level + 1, 6)
                lines.append(f"{header_prefix} {section.title}")
                lines.append("")
                
                if section.content:
                    # Process content
                    content = self._process_content(section.content)
                    lines.append(content)
                    lines.append("")
        else:
            # No sections, just add raw content
            content = self._process_content(parsed.content)
            lines.append(content)
        
        # Add tables
        if parsed.tables and options.get('preserve_tables', True):
            for table in parsed.tables:
                lines.append(self._table_to_markdown(table))
                lines.append("")
        
        # Add links section if there are many links
        if len(parsed.links) > 5:
            lines.append("## Links")
            lines.append("")
            for link in parsed.links:
                lines.append(f"- [{link.get('text', link['url'])}]({link['url']})")
            lines.append("")
        
        return '\n'.join(lines)
    
    def _process_content(self, content: str) -> str:
        """Process and clean content for Markdown"""
        # Remove excessive whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Escape special Markdown characters
        content = self._escape_markdown(content)
        
        # Format lists
        content = self._format_lists(content)
        
        # Format code blocks
        content = self._format_code_blocks(content)
        
        return content.strip()
    
    def _escape_markdown(self, text: str) -> str:
        """Escape special Markdown characters"""
        # Don't escape inside code blocks
        parts = []
        in_code = False
        
        for line in text.split('\n'):
            if line.strip().startswith('```'):
                in_code = not in_code
                parts.append(line)
            elif not in_code:
                # Escape special characters
                line = line.replace('\\', '\\\\')
                line = line.replace('*', '\\*')
                line = line.replace('_', '\\_')
                line = line.replace('[', '\\[')
                line = line.replace(']', '\\]')
                parts.append(line)
            else:
                parts.append(line)
        
        return '\n'.join(parts)
    
    def _format_lists(self, content: str) -> str:
        """Format list items"""
        lines = content.split('\n')
        formatted = []
        
        for line in lines:
            stripped = line.strip()
            
            # Numbered list
            if re.match(r'^\d+[.\)]\s', stripped):
                formatted.append(line)
            # Bullet list
            elif re.match(r'^[•\-\*]\s', stripped):
                formatted.append(re.sub(r'^[•\-\*]', '-', line))
            else:
                formatted.append(line)
        
        return '\n'.join(formatted)
    
    def _format_code_blocks(self, content: str) -> str:
        """Format code blocks"""
        # Already in Markdown format, just ensure proper spacing
        return content
    
    def _table_to_markdown(self, table: List[List[str]]) -> str:
        """Convert table data to Markdown table"""
        if not table or not table[0]:
            return ""
        
        lines = []
        
        # Header row
        header = table[0]
        lines.append("| " + " | ".join(header) + " |")
        
        # Separator
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        
        # Data rows
        for row in table[1:]:
            # Pad row to match header length
            while len(row) < len(header):
                row.append("")
            lines.append("| " + " | ".join(row[:len(header)]) + " |")
        
        return '\n'.join(lines)
    
    def _to_anchor(self, text: str) -> str:
        """Convert text to Markdown anchor"""
        # Remove special characters and convert to lowercase
        anchor = re.sub(r'[^\w\s-]', '', text.lower())
        anchor = re.sub(r'\s+', '-', anchor)
        return anchor
    
    def batch_convert(self, file_paths: List[Union[str, Path]], 
                      output_dir: Union[str, Path],
                      **options) -> Dict[str, str]:
        """
        Convert multiple files to Markdown
        
        Args:
            file_paths: List of file paths to convert
            output_dir: Directory to save converted files
            **options: Conversion options
            
        Returns:
            Dictionary mapping input paths to output paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        for file_path in file_paths:
            file_path = Path(file_path)
            
            try:
                markdown = self.convert(file_path, **options)
                
                # Generate output filename
                output_name = file_path.stem + ".md"
                output_path = output_dir / output_name
                
                # Write file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown)
                
                results[str(file_path)] = str(output_path)
                
            except Exception as e:
                results[str(file_path)] = f"Error: {str(e)}"
        
        return results
    
    def convert_to_file(self, file_path: Union[str, Path], 
                        output_path: Union[str, Path],
                        **options) -> str:
        """
        Convert a document and save to file
        
        Args:
            file_path: Input document path
            output_path: Output Markdown file path
            **options: Conversion options
            
        Returns:
            Path to output file
        """
        markdown = self.convert(file_path, **options)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        return str(output_path)
