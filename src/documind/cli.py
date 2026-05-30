"""
Command Line Interface
命令行接口

Main entry point for DocuMind CLI tool.
DocuMind CLI工具的主入口。
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Optional, List

from . import __version__
from .parser import DocumentParser, ParsedDocument
from .converter import MarkdownConverter
from .extractor import StructuredExtractor
from .analyzer import DocumentAnalyzer


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog='documind',
        description='''
DocuMind - Lightweight AI Document Intelligence Parser
轻量级AI文档智能解析工具

Convert, extract, and analyze documents with ease.
轻松转换、提取和分析文档。
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'DocuMind {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Parse command
    parse_parser = subparsers.add_parser(
        'parse',
        help='Parse a document and extract structure',
        description='Parse documents and extract structured content'
    )
    parse_parser.add_argument('input', help='Input file path')
    parse_parser.add_argument('-o', '--output', help='Output file path (JSON)')
    parse_parser.add_argument('--format', choices=['json', 'txt'], default='json',
                             help='Output format')
    
    # Convert command
    convert_parser = subparsers.add_parser(
        'convert',
        help='Convert document to Markdown',
        description='Convert various document formats to Markdown'
    )
    convert_parser.add_argument('input', help='Input file path')
    convert_parser.add_argument('-o', '--output', help='Output file path')
    convert_parser.add_argument('--toc', action='store_true',
                               help='Include table of contents')
    convert_parser.add_argument('--metadata', action='store_true',
                               help='Include YAML frontmatter')
    
    # Extract command
    extract_parser = subparsers.add_parser(
        'extract',
        help='Extract structured data from documents',
        description='Extract emails, URLs, dates, and more'
    )
    extract_parser.add_argument('input', help='Input file path')
    extract_parser.add_argument('-o', '--output', help='Output file path')
    extract_parser.add_argument('-t', '--type', 
                               choices=['email', 'url', 'phone', 'date', 'all'],
                               default='all',
                               help='Type of data to extract')
    extract_parser.add_argument('--format', choices=['json', 'csv'], default='json',
                               help='Output format')
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze document content',
        description='Analyze document statistics, keywords, and sentiment'
    )
    analyze_parser.add_argument('input', help='Input file path')
    analyze_parser.add_argument('-o', '--output', help='Output file path')
    analyze_parser.add_argument('--format', choices=['json', 'markdown'], default='markdown',
                               help='Output format')
    
    # Batch command
    batch_parser = subparsers.add_parser(
        'batch',
        help='Batch process multiple files',
        description='Process multiple files in one command'
    )
    batch_parser.add_argument('input', nargs='+', help='Input file paths')
    batch_parser.add_argument('-o', '--output-dir', required=True,
                             help='Output directory')
    batch_parser.add_argument('--command', choices=['parse', 'convert', 'extract'],
                             required=True, help='Command to run on each file')
    
    return parser


def cmd_parse(args) -> int:
    """Handle parse command"""
    try:
        parser = DocumentParser()
        parsed = parser.parse(args.input)
        
        if args.format == 'json':
            output = parsed.to_json()
        else:
            output = parsed.content
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✅ Output saved to: {args.output}")
        else:
            print(output)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_convert(args) -> int:
    """Handle convert command"""
    try:
        converter = MarkdownConverter()
        
        options = {
            'include_toc': args.toc,
            'include_metadata': args.metadata
        }
        
        markdown = converter.convert(args.input, **options)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"✅ Markdown saved to: {args.output}")
        else:
            print(markdown)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_extract(args) -> int:
    """Handle extract command"""
    try:
        extractor = StructuredExtractor()
        
        patterns = None if args.type == 'all' else [args.type]
        results = extractor.extract_from_file(args.input, patterns)
        
        if args.format == 'json':
            output = json.dumps(results, indent=2, ensure_ascii=False)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"✅ Extracted data saved to: {args.output}")
            else:
                print(output)
        else:
            # CSV format
            if args.output:
                extractor.export_to_csv(results, args.output)
                print(f"✅ Extracted data saved to: {args.output}")
            else:
                # Print CSV to stdout
                for data_type, values in results.items():
                    for value in values:
                        print(f"{data_type},{value}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_analyze(args) -> int:
    """Handle analyze command"""
    try:
        analyzer = DocumentAnalyzer()
        
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
        
        report = analyzer.generate_report(text, output_format=args.format)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Analysis report saved to: {args.output}")
        else:
            print(report)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def cmd_batch(args) -> int:
    """Handle batch command"""
    try:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        success_count = 0
        error_count = 0
        
        for input_path in args.input:
            input_path = Path(input_path)
            
            if not input_path.exists():
                print(f"⚠️  Skipping non-existent file: {input_path}")
                error_count += 1
                continue
            
            try:
                output_path = output_dir / f"{input_path.stem}.md"
                
                if args.command == 'parse':
                    parser = DocumentParser()
                    parsed = parser.parse(input_path)
                    output_path = output_dir / f"{input_path.stem}.json"
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(parsed.to_json())
                        
                elif args.command == 'convert':
                    converter = MarkdownConverter()
                    converter.convert_to_file(input_path, output_path)
                    
                elif args.command == 'extract':
                    extractor = StructuredExtractor()
                    results = extractor.extract_from_file(input_path)
                    output_path = output_dir / f"{input_path.stem}_extracted.json"
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(results, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Processed: {input_path} -> {output_path}")
                success_count += 1
                
            except Exception as e:
                print(f"❌ Error processing {input_path}: {e}")
                error_count += 1
        
        print(f"\n📊 Batch processing complete: {success_count} succeeded, {error_count} failed")
        return 0 if error_count == 0 else 1
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    if not parsed_args.command:
        parser.print_help()
        return 0
    
    # Dispatch to appropriate command handler
    commands = {
        'parse': cmd_parse,
        'convert': cmd_convert,
        'extract': cmd_extract,
        'analyze': cmd_analyze,
        'batch': cmd_batch,
    }
    
    handler = commands.get(parsed_args.command)
    if handler:
        return handler(parsed_args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
