"""
Structured Data Extractor Module
结构化数据提取模块

Extracts structured data from documents using intelligent pattern matching.
使用智能模式匹配从文档中提取结构化数据。
"""

import re
import json
from typing import Dict, List, Optional, Union, Any, Callable
from dataclasses import dataclass, field
from pathlib import Path
from .parser import ParsedDocument, DocumentParser


@dataclass
class ExtractionRule:
    """Defines a rule for extracting data"""
    name: str
    pattern: str
    data_type: str = "text"  # text, number, date, email, url, list
    multiple: bool = False
    transform: Optional[Callable[[str], Any]] = None
    
    def extract(self, text: str) -> Union[str, List[str], None]:
        """Apply extraction rule to text"""
        matches = re.findall(self.pattern, text, re.IGNORECASE | re.MULTILINE)
        
        if not matches:
            return [] if self.multiple else None
        
        # Apply transform if provided
        if self.transform:
            matches = [self.transform(m) for m in matches]
        
        if self.multiple:
            return matches
        else:
            return matches[0] if matches else None


@dataclass
class ExtractionResult:
    """Result of structured data extraction"""
    rule_name: str
    values: Union[str, List[str], None]
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_name": self.rule_name,
            "values": self.values,
            "confidence": self.confidence
        }


class StructuredExtractor:
    """
    Structured data extractor from documents
    
    Features:
    - Predefined extraction patterns (emails, URLs, dates, etc.)
    - Custom extraction rule support
    - JSON/CSV output formats
    - Batch extraction capabilities
    """
    
    # Predefined extraction patterns
    PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'url': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?',
        'phone': r'(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
        'date_iso': r'\d{4}-\d{2}-\d{2}',
        'date_us': r'\d{1,2}/\d{1,2}/\d{2,4}',
        'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        'hex_color': r'#[0-9A-Fa-f]{6}\b',
        'hashtag': r'#\w+',
        'mention': r'@\w+',
        'money': r'\$[\d,]+(?:\.\d{2})?',
        'percentage': r'\d+(?:\.\d+)?%',
    }
    
    def __init__(self):
        self.parser = DocumentParser()
        self.custom_rules: List[ExtractionRule] = []
    
    def extract(self, text: str, patterns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Extract structured data from text
        
        Args:
            text: Input text to extract from
            patterns: List of pattern names to use (default: all)
            
        Returns:
            Dictionary of extracted data
        """
        if patterns is None:
            patterns = list(self.PATTERNS.keys())
        
        results = {}
        
        for pattern_name in patterns:
            if pattern_name in self.PATTERNS:
                pattern = self.PATTERNS[pattern_name]
                matches = re.findall(pattern, text, re.IGNORECASE)
                
                if matches:
                    # Remove duplicates while preserving order
                    seen = set()
                    unique_matches = []
                    for match in matches:
                        if match not in seen:
                            seen.add(match)
                            unique_matches.append(match)
                    
                    results[pattern_name] = unique_matches
        
        # Apply custom rules
        for rule in self.custom_rules:
            value = rule.extract(text)
            if value:
                results[rule.name] = value
        
        return results
    
    def extract_from_file(self, file_path: Union[str, Path], 
                          patterns: Optional[List[str]] = None) -> Dict[str, Any]:
        """Extract data from a document file"""
        parsed = self.parser.parse(file_path)
        
        # Combine all content
        all_content = parsed.content
        for section in parsed.sections:
            all_content += "\n" + section.content
        
        return self.extract(all_content, patterns)
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text
        
        Returns entities categorized by type:
        - persons
        - organizations
        - locations
        - products
        """
        entities = {
            "persons": [],
            "organizations": [],
            "locations": [],
            "products": []
        }
        
        # Simple heuristic-based entity extraction
        # Capitalized words sequences (potential proper nouns)
        proper_noun_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
        candidates = re.findall(proper_noun_pattern, text)
        
        # Common organization indicators
        org_indicators = ['Inc', 'Corp', 'Ltd', 'LLC', 'Company', 'Corporation', 
                         'Organization', 'Institute', 'University', 'College']
        
        # Common location indicators
        loc_indicators = ['Street', 'Avenue', 'Road', 'City', 'Town', 'State',
                         'Country', 'Mountain', 'River', 'Lake', 'Park']
        
        seen = set()
        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            
            words = candidate.split()
            last_word = words[-1] if words else ""
            
            if any(ind in last_word for ind in org_indicators):
                entities["organizations"].append(candidate)
            elif any(ind in last_word for ind in loc_indicators):
                entities["locations"].append(candidate)
            elif len(words) >= 2:
                # Likely a person's name
                entities["persons"].append(candidate)
        
        return entities
    
    def extract_key_value_pairs(self, text: str, 
                                 separator: str = r':',
                                 delimiter: str = r'\n') -> Dict[str, str]:
        """
        Extract key-value pairs from text
        
        Args:
            text: Input text
            separator: Pattern separating key from value
            delimiter: Pattern separating pairs
            
        Returns:
            Dictionary of key-value pairs
        """
        pairs = {}
        
        # Pattern: Key: Value
        pattern = rf'^\s*(.+?)\s*{separator}\s*(.+?)\s*(?:{delimiter}|$)'
        matches = re.findall(pattern, text, re.MULTILINE)
        
        for key, value in matches:
            key = key.strip()
            value = value.strip()
            if key and value:
                pairs[key] = value
        
        return pairs
    
    def extract_tables(self, text: str) -> List[List[List[str]]]:
        """
        Extract tables from text
        
        Supports:
        - Markdown tables
        - CSV-like tables
        - Whitespace-aligned tables
        """
        tables = []
        
        # Markdown table pattern
        md_pattern = r'\|(.+?)\|\n\|[-:\s|]+\|\n((?:\|.+?\|\n?)+)'
        md_matches = re.findall(md_pattern, text)
        
        for header, rows in md_matches:
            table = []
            # Parse header
            header_cells = [cell.strip() for cell in header.split('|') if cell.strip()]
            table.append(header_cells)
            
            # Parse rows
            for row in rows.strip().split('\n'):
                cells = [cell.strip() for cell in row.split('|') if cell.strip()]
                if cells:
                    table.append(cells)
            
            tables.append(table)
        
        return tables
    
    def add_custom_rule(self, name: str, pattern: str, 
                        data_type: str = "text",
                        multiple: bool = False,
                        transform: Optional[Callable[[str], Any]] = None):
        """Add a custom extraction rule"""
        rule = ExtractionRule(
            name=name,
            pattern=pattern,
            data_type=data_type,
            multiple=multiple,
            transform=transform
        )
        self.custom_rules.append(rule)
    
    def export_to_json(self, data: Dict[str, Any], 
                       output_path: Optional[Union[str, Path]] = None) -> str:
        """Export extracted data to JSON"""
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str
    
    def export_to_csv(self, data: Dict[str, List[str]], 
                      output_path: Union[str, Path]) -> str:
        """Export extracted data to CSV format"""
        lines = ["Type,Value"]
        
        for data_type, values in data.items():
            for value in values:
                # Escape commas and quotes
                value = str(value).replace('"', '""')
                if ',' in value:
                    value = f'"{value}"'
                lines.append(f"{data_type},{value}")
        
        csv_content = '\n'.join(lines)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        return str(output_path)
    
    def batch_extract(self, file_paths: List[Union[str, Path]], 
                      patterns: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
        """
        Extract data from multiple files
        
        Args:
            file_paths: List of file paths
            patterns: Patterns to extract
            
        Returns:
            Dictionary mapping file paths to extraction results
        """
        results = {}
        
        for file_path in file_paths:
            try:
                results[str(file_path)] = self.extract_from_file(file_path, patterns)
            except Exception as e:
                results[str(file_path)] = {"error": str(e)}
        
        return results
