<div align="center">

# 🧠 DocuMind

**Lightweight AI Document Intelligence Parser**

**轻量级AI文档智能解析工具**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)](https://github.com/yourusername/documind)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg)](requirements.txt)

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🎉 Project Introduction

DocuMind is a **zero-dependency**, **local-first** document parsing and structured data extraction tool. Inspired by popular projects like Microsoft's markitdown and LlamaIndex's liteparse, DocuMind focuses on providing a lightweight, fast, and intelligent document processing solution.

### ✨ Key Differentiators

- 🚀 **Zero Dependencies**: Uses only Python standard library - no external packages required
- 🔒 **Privacy First**: All processing happens locally - your data never leaves your machine
- ⚡ **Lightning Fast**: Optimized for speed with minimal resource usage
- 🎯 **Multi-Format Support**: Handles TXT, MD, HTML, JSON, CSV, XML, and more
- 🤖 **AI-Ready Output**: Structured output perfect for LLM consumption

---

## ✨ Core Features

| Feature | Description | Emoji |
|---------|-------------|-------|
| **Document Parsing** | Extract structure from multiple formats | 📄 |
| **Markdown Conversion** | Convert any document to clean Markdown | 📝 |
| **Data Extraction** | Extract emails, URLs, dates, entities | 🔍 |
| **Content Analysis** | Statistics, keywords, sentiment, topics | 📊 |
| **Batch Processing** | Process multiple files efficiently | 🔄 |
| **CLI Interface** | Easy-to-use command-line tool | 💻 |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/documind.git
cd documind

# Install the package
pip install -e .
```

### Basic Usage

```bash
# Parse a document
documind parse document.txt

# Convert to Markdown
documind convert document.html -o output.md

# Extract structured data
documind extract document.txt -o data.json

# Analyze content
documind analyze document.txt -o report.md

# Batch process
documind batch file1.txt file2.md file3.html -o ./output --command convert
```

---

## 📖 Detailed Usage Guide

### Document Parsing

```python
from documind import DocumentParser

parser = DocumentParser()
doc = parser.parse("document.md")

print(f"Title: {doc.title}")
print(f"Sections: {len(doc.sections)}")
print(doc.to_json())
```

### Markdown Conversion

```python
from documind import MarkdownConverter

converter = MarkdownConverter()
markdown = converter.convert("document.html", include_toc=True)
print(markdown)
```

### Data Extraction

```python
from documind import StructuredExtractor

extractor = StructuredExtractor()
data = extractor.extract_from_file("document.txt")

print(f"Emails found: {data.get('email', [])}")
print(f"URLs found: {data.get('url', [])}")
```

### Document Analysis

```python
from documind import DocumentAnalyzer

analyzer = DocumentAnalyzer()
report = analyzer.analyze_file("document.txt")

print(f"Word count: {report['statistics']['word_count']}")
print(f"Sentiment: {report['sentiment']['sentiment']}")
```

---

## 💡 Design Philosophy

### Why DocuMind?

1. **Simplicity**: No complex setup or dependencies
2. **Speed**: Optimized for performance
3. **Privacy**: Local processing only
4. **Flexibility**: Works with any Python environment

### Technical Choices

- **Pure Python**: Maximum compatibility
- **Standard Library Only**: Zero dependency overhead
- **Modular Design**: Use only what you need
- **Type Hints**: Full type safety support

---

## 📦 Packaging & Deployment

### Build Package

```bash
# Build wheel
python -m build

# Install locally
pip install dist/documind-1.0.0-py3-none-any.whl
```

### Run Tests

```bash
# Run all tests
python -m unittest discover tests/ -v

# Run specific test
python -m unittest tests.test_parser
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Convention

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation updates
- `refactor:` Code refactoring
- `test:` Test additions/updates

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🎉 项目介绍

DocuMind 是一个**零依赖**、**本地优先**的文档解析与结构化数据提取工具。灵感来自 Microsoft 的 markitdown 和 LlamaIndex 的 liteparse 等热门项目，DocuMind 专注于提供轻量级、快速、智能的文档处理解决方案。

### ✨ 核心差异化亮点

- 🚀 **零依赖设计**: 仅使用 Python 标准库 - 无需外部包
- 🔒 **隐私优先**: 所有处理都在本地完成 - 数据永不离开您的机器
- ⚡ **极速处理**: 针对速度优化，资源占用极低
- 🎯 **多格式支持**: 支持 TXT、MD、HTML、JSON、CSV、XML 等格式
- 🤖 **AI就绪输出**: 结构化输出，完美适配大语言模型

---

## ✨ 核心特性

| 特性 | 描述 | 图标 |
|------|------|------|
| **文档解析** | 从多种格式提取文档结构 | 📄 |
| **Markdown转换** | 将任何文档转换为干净的 Markdown | 📝 |
| **数据提取** | 提取邮箱、URL、日期、实体 | 🔍 |
| **内容分析** | 统计、关键词、情感、主题分析 | 📊 |
| **批量处理** | 高效处理多个文件 | 🔄 |
| **CLI界面** | 易于使用的命令行工具 | 💻 |

---

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/documind.git
cd documind

# 安装包
pip install -e .
```

### 基本用法

```bash
# 解析文档
documind parse document.txt

# 转换为 Markdown
documind convert document.html -o output.md

# 提取结构化数据
documind extract document.txt -o data.json

# 分析内容
documind analyze document.txt -o report.md

# 批量处理
documind batch file1.txt file2.md file3.html -o ./output --command convert
```

---

## 📖 详细使用指南

### 文档解析

```python
from documind import DocumentParser

parser = DocumentParser()
doc = parser.parse("document.md")

print(f"标题: {doc.title}")
print(f"章节数: {len(doc.sections)}")
print(doc.to_json())
```

### Markdown 转换

```python
from documind import MarkdownConverter

converter = MarkdownConverter()
markdown = converter.convert("document.html", include_toc=True)
print(markdown)
```

### 数据提取

```python
from documind import StructuredExtractor

extractor = StructuredExtractor()
data = extractor.extract_from_file("document.txt")

print(f"找到的邮箱: {data.get('email', [])}")
print(f"找到的URL: {data.get('url', [])}")
```

### 文档分析

```python
from documind import DocumentAnalyzer

analyzer = DocumentAnalyzer()
report = analyzer.analyze_file("document.txt")

print(f"字数: {report['statistics']['word_count']}")
print(f"情感: {report['sentiment']['sentiment']}")
```

---

## 💡 设计理念

### 为什么选择 DocuMind？

1. **简洁性**: 无需复杂设置或依赖
2. **速度**: 性能优化
3. **隐私**: 纯本地处理
4. **灵活性**: 适用于任何 Python 环境

### 技术选型

- **纯 Python**: 最大兼容性
- **仅标准库**: 零依赖开销
- **模块化设计**: 按需使用
- **类型提示**: 完整类型安全支持

---

## 📦 打包与部署

### 构建包

```bash
# 构建 wheel
python -m build

# 本地安装
pip install dist/documind-1.0.0-py3-none-any.whl
```

### 运行测试

```bash
# 运行所有测试
python -m unittest discover tests/ -v

# 运行特定测试
python -m unittest tests.test_parser
```

---

## 🤝 贡献指南

欢迎贡献！请遵循以下准则：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 提交规范

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试添加/更新

---

## 📄 开源协议

本项目采用 MIT 协议开源 - 详情请参见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🎉 專案介紹

DocuMind 是一個**零依賴**、**本地優先**的文件解析與結構化資料提取工具。靈感來自 Microsoft 的 markitdown 和 LlamaIndex 的 liteparse 等熱門專案，DocuMind 專注於提供輕量級、快速、智慧的文件處理解決方案。

### ✨ 核心差異化亮點

- 🚀 **零依賴設計**: 僅使用 Python 標準庫 - 無需外部套件
- 🔒 **隱私優先**: 所有處理都在本地完成 - 資料永不離開您的機器
- ⚡ **極速處理**: 針對速度優化，資源占用極低
- 🎯 **多格式支援**: 支援 TXT、MD、HTML、JSON、CSV、XML 等格式
- 🤖 **AI就緒輸出**: 結構化輸出，完美適配大語言模型

---

## ✨ 核心特性

| 特性 | 描述 | 圖示 |
|------|------|------|
| **文件解析** | 從多種格式提取文件結構 | 📄 |
| **Markdown轉換** | 將任何文件轉換為乾淨的 Markdown | 📝 |
| **資料提取** | 提取郵箱、URL、日期、實體 | 🔍 |
| **內容分析** | 統計、關鍵詞、情感、主題分析 | 📊 |
| **批次處理** | 高效處理多個文件 | 🔄 |
| **CLI介面** | 易於使用的命令列工具 | 💻 |

---

## 🚀 快速開始

### 安裝

```bash
# 克隆倉庫
git clone https://github.com/yourusername/documind.git
cd documind

# 安裝套件
pip install -e .
```

### 基本用法

```bash
# 解析文件
documind parse document.txt

# 轉換為 Markdown
documind convert document.html -o output.md

# 提取結構化資料
documind extract document.txt -o data.json

# 分析內容
documind analyze document.txt -o report.md

# 批次處理
documind batch file1.txt file2.md file3.html -o ./output --command convert
```

---

## 📖 詳細使用指南

### 文件解析

```python
from documind import DocumentParser

parser = DocumentParser()
doc = parser.parse("document.md")

print(f"標題: {doc.title}")
print(f"章節數: {len(doc.sections)}")
print(doc.to_json())
```

### Markdown 轉換

```python
from documind import MarkdownConverter

converter = MarkdownConverter()
markdown = converter.convert("document.html", include_toc=True)
print(markdown)
```

### 資料提取

```python
from documind import StructuredExtractor

extractor = StructuredExtractor()
data = extractor.extract_from_file("document.txt")

print(f"找到的郵箱: {data.get('email', [])}")
print(f"找到的URL: {data.get('url', [])}")
```

### 文件分析

```python
from documind import DocumentAnalyzer

analyzer = DocumentAnalyzer()
report = analyzer.analyze_file("document.txt")

print(f"字數: {report['statistics']['word_count']}")
print(f"情感: {report['sentiment']['sentiment']}")
```

---

## 💡 設計理念

### 為什麼選擇 DocuMind？

1. **簡潔性**: 無需複雜設定或依賴
2. **速度**: 效能優化
3. **隱私**: 純本地處理
4. **靈活性**: 適用於任何 Python 環境

### 技術選型

- **純 Python**: 最大相容性
- **僅標準庫**: 零依賴開銷
- **模組化設計**: 按需使用
- **類型提示**: 完整類型安全支援

---

## 📦 打包與部署

### 構建套件

```bash
# 構建 wheel
python -m build

# 本地安裝
pip install dist/documind-1.0.0-py3-none-any.whl
```

### 執行測試

```bash
# 執行所有測試
python -m unittest discover tests/ -v

# 執行特定測試
python -m unittest tests.test_parser
```

---

## 🤝 貢獻指南

歡迎貢獻！請遵循以下準則：

1. Fork 本倉庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 建立 Pull Request

### 提交規範

- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文件更新
- `refactor:` 程式碼重構
- `test:` 測試新增/更新

---

## 📄 開源協議

本專案採用 MIT 協議開源 - 詳情請參見 [LICENSE](LICENSE) 文件。

---

<div align="center">

**Made with ❤️ by DocuMind Team**

⭐ Star us on GitHub if you find this project helpful!

</div>
