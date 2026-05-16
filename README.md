<div align="center">

# 📚 DocuMind

**Lightweight Document Intelligence Processing Engine**

**轻量级文档智能处理引擎**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🎉 Introduction

**DocuMind** is a lightweight, zero-dependency document intelligence processing engine that transforms complex documents into structured knowledge. Built with pure Python standard library, it provides powerful document analysis capabilities without requiring any external dependencies.

### 💡 Why DocuMind?

- **🚀 Zero Dependencies**: Uses only Python standard library - no pip install nightmares
- **📄 Multi-Format Support**: PDF, TXT, Markdown, DOCX out of the box
- **🧠 Intelligent Analysis**: Automatic summarization, keyword extraction, knowledge graph generation
- **⚡ Lightweight & Fast**: Minimal resource footprint, blazing fast processing
- **🎯 Developer-Friendly**: Clean API, TUI interface, easy to integrate

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📖 **Multi-Format Parsing** | Extract content from PDF, TXT, Markdown, DOCX files |
| 📝 **Smart Summarization** | Generate concise document summaries using TF-IDF |
| 🔑 **Keyword Extraction** | Identify important terms and concepts automatically |
| 🕸️ **Knowledge Graph** | Build entity relationship graphs from documents |
| 📊 **Metadata Extraction** | Extract titles, headings, code blocks, tables, links |
| 🗂️ **Batch Processing** | Process entire directories recursively |
| 🖥️ **TUI Interface** | Beautiful terminal UI with progress bars and colors |
| 📤 **JSON Export** | Export results for further analysis |

---

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- No external dependencies required!

### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/DocuMind.git
cd DocuMind

# Or install via pip (when published)
pip install documind
```

### Usage

```bash
# Process a single file
python documind.py document.pdf

# Process with all features
python documind.py article.md --knowledge-graph --output result.json

# Batch process directory
python documind.py ./documents --recursive --output batch_results.json

# Skip summary generation
python documind.py report.txt --no-summary
```

---

## 📖 Detailed Usage Guide

### Command-Line Options

```bash
python documind.py [INPUT] [OPTIONS]

Arguments:
  INPUT                 Input file or directory

Options:
  -r, --recursive       Process directories recursively
  -o, --output FILE     Export results to JSON file
  --no-summary          Skip summary generation
  --no-keywords         Skip keyword extraction
  -k, --knowledge-graph Build knowledge graph
  -v, --version         Show version information
  -h, --help            Show help message
```

### Python API

```python
from documind import DocumentProcessor

# Initialize processor
processor = DocumentProcessor()

# Process single file
result = processor.process_file("document.pdf", {
    'summarize': True,
    'keywords': True,
    'knowledge_graph': True
})

# Access results
print(result['summary'])
print(result['keywords'])
print(result['knowledge_graph'])

# Batch process
results = processor.process_directory("./docs", recursive=True)
```

### Supported Formats

| Format | Extension | Features |
|--------|-----------|----------|
| Plain Text | `.txt` | Full support |
| Markdown | `.md`, `.markdown` | Headings, code blocks, links, lists, tables |
| PDF | `.pdf` | Text extraction |
| Word | `.docx` | Text extraction |

---

## 💡 Design Philosophy

### Zero-Dependency Architecture

DocuMind is built entirely on Python's standard library:
- **PDF Parsing**: Custom binary parser without PyPDF2
- **DOCX Parsing**: ZIP/XML parser without python-docx
- **Text Analysis**: Custom TF-IDF without scikit-learn
- **TUI**: ANSI escape codes without rich/curses

### Performance Optimized

- Streaming processing for large files
- Memory-efficient text analysis
- Parallel processing support (future)

---

## 📦 Packaging & Deployment

### Build Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build standalone executable
pyinstaller --onefile --name documind documind.py
```

### Install as Package

```bash
pip install -e .

# Then use globally
documind document.pdf
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Message Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build/tooling changes

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🎉 项目介绍

**DocuMind** 是一款轻量级、零依赖的文档智能处理引擎，能够将复杂的文档转换为结构化的知识。完全基于 Python 标准库构建，无需任何外部依赖即可提供强大的文档分析能力。

### 💡 为什么选择 DocuMind？

- **🚀 零依赖**: 仅使用 Python 标准库 - 告别 pip 安装噩梦
- **📄 多格式支持**: 开箱即用支持 PDF、TXT、Markdown、DOCX
- **🧠 智能分析**: 自动摘要、关键词提取、知识图谱生成
- **⚡ 轻量快速**: 极小的资源占用，闪电般的处理速度
- **🎯 开发者友好**: 简洁的 API、TUI 界面、易于集成

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📖 **多格式解析** | 从 PDF、TXT、Markdown、DOCX 文件中提取内容 |
| 📝 **智能摘要** | 使用 TF-IDF 生成简洁的文档摘要 |
| 🔑 **关键词提取** | 自动识别重要术语和概念 |
| 🕸️ **知识图谱** | 从文档构建实体关系图谱 |
| 📊 **元数据提取** | 提取标题、标题、代码块、表格、链接 |
| 🗂️ **批量处理** | 递归处理整个目录 |
| 🖥️ **TUI 界面** | 美观的终端界面，带进度条和颜色 |
| 📤 **JSON 导出** | 导出结果以供进一步分析 |

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 无需外部依赖！

### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/DocuMind.git
cd DocuMind

# 或通过 pip 安装（发布后）
pip install documind
```

### 使用方法

```bash
# 处理单个文件
python documind.py document.pdf

# 使用所有功能
python documind.py article.md --knowledge-graph --output result.json

# 批量处理目录
python documind.py ./documents --recursive --output batch_results.json

# 跳过摘要生成
python documind.py report.txt --no-summary
```

---

## 📖 详细使用指南

### 命令行选项

```bash
python documind.py [输入] [选项]

参数:
  输入                  输入文件或目录

选项:
  -r, --recursive       递归处理目录
  -o, --output 文件     导出结果到 JSON 文件
  --no-summary          跳过摘要生成
  --no-keywords         跳过关键词提取
  -k, --knowledge-graph 构建知识图谱
  -v, --version         显示版本信息
  -h, --help            显示帮助信息
```

### Python API

```python
from documind import DocumentProcessor

# 初始化处理器
processor = DocumentProcessor()

# 处理单个文件
result = processor.process_file("document.pdf", {
    'summarize': True,
    'keywords': True,
    'knowledge_graph': True
})

# 访问结果
print(result['summary'])
print(result['keywords'])
print(result['knowledge_graph'])

# 批量处理
results = processor.process_directory("./docs", recursive=True)
```

### 支持的格式

| 格式 | 扩展名 | 特性 |
|------|--------|------|
| 纯文本 | `.txt` | 完全支持 |
| Markdown | `.md`, `.markdown` | 标题、代码块、链接、列表、表格 |
| PDF | `.pdf` | 文本提取 |
| Word | `.docx` | 文本提取 |

---

## 💡 设计理念

### 零依赖架构

DocuMind 完全基于 Python 标准库构建：
- **PDF 解析**: 自定义二进制解析器，无需 PyPDF2
- **DOCX 解析**: ZIP/XML 解析器，无需 python-docx
- **文本分析**: 自定义 TF-IDF，无需 scikit-learn
- **TUI**: ANSI 转义码，无需 rich/curses

### 性能优化

- 大文件流式处理
- 内存高效的文本分析
- 支持并行处理（未来）

---

## 📦 打包与部署

### 构建可执行文件

```bash
# 安装 PyInstaller
pip install pyinstaller

# 构建独立可执行文件
pyinstaller --onefile --name documind documind.py
```

### 作为包安装

```bash
pip install -e .

# 然后全局使用
documind document.pdf
```

---

## 🤝 贡献指南

我们欢迎贡献！请遵循以下准则：

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

### 提交信息规范

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更改
- `refactor:` 代码重构
- `test:` 测试更改
- `chore:` 构建/工具更改

---

## 📄 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

<a name="繁體中文"></a>
## 🎉 專案介紹

**DocuMind** 是一款輕量級、零依賴的文件智慧處理引擎，能夠將複雜的文件轉換為結構化的知識。完全基於 Python 標準庫構建，無需任何外部依賴即可提供強大的文件分析能力。

### 💡 為什麼選擇 DocuMind？

- **🚀 零依賴**: 僅使用 Python 標準庫 - 告別 pip 安裝噩夢
- **📄 多格式支援**: 開箱即用支援 PDF、TXT、Markdown、DOCX
- **🧠 智慧分析**: 自動摘要、關鍵詞提取、知識圖譜生成
- **⚡ 輕量快速**: 極小的資源佔用，閃電般的處理速度
- **🎯 開發者友好**: 簡潔的 API、TUI 介面、易於整合

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📖 **多格式解析** | 從 PDF、TXT、Markdown、DOCX 文件中提取內容 |
| 📝 **智慧摘要** | 使用 TF-IDF 生成簡潔的文件摘要 |
| 🔑 **關鍵詞提取** | 自動識別重要術語和概念 |
| 🕸️ **知識圖譜** | 從文件構建實體關係圖譜 |
| 📊 **元資料提取** | 提取標題、標題、程式碼塊、表格、連結 |
| 🗂️ **批次處理** | 遞迴處理整個目錄 |
| 🖥️ **TUI 介面** | 美觀的終端介面，帶進度條和顏色 |
| 📤 **JSON 匯出** | 匯出結果以供進一步分析 |

---

## 🚀 快速開始

### 環境要求

- Python 3.8 或更高版本
- 無需外部依賴！

### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/DocuMind.git
cd DocuMind

# 或透過 pip 安裝（發布後）
pip install documind
```

### 使用方法

```bash
# 處理單個文件
python documind.py document.pdf

# 使用所有功能
python documind.py article.md --knowledge-graph --output result.json

# 批次處理目錄
python documind.py ./documents --recursive --output batch_results.json

# 跳過摘要生成
python documind.py report.txt --no-summary
```

---

## 📖 詳細使用指南

### 命令列選項

```bash
python documind.py [輸入] [選項]

參數:
  輸入                  輸入文件或目錄

選項:
  -r, --recursive       遞迴處理目錄
  -o, --output 檔案     匯出結果到 JSON 檔案
  --no-summary          跳過摘要生成
  --no-keywords         跳過關鍵詞提取
  -k, --knowledge-graph 構建知識圖譜
  -v, --version         顯示版本資訊
  -h, --help            顯示幫助資訊
```

### Python API

```python
from documind import DocumentProcessor

# 初始化處理器
processor = DocumentProcessor()

# 處理單個文件
result = processor.process_file("document.pdf", {
    'summarize': True,
    'keywords': True,
    'knowledge_graph': True
})

# 訪問結果
print(result['summary'])
print(result['keywords'])
print(result['knowledge_graph'])

# 批次處理
results = processor.process_directory("./docs", recursive=True)
```

### 支援的格式

| 格式 | 擴展名 | 特性 |
|------|--------|------|
| 純文字 | `.txt` | 完全支援 |
| Markdown | `.md`, `.markdown` | 標題、程式碼塊、連結、列表、表格 |
| PDF | `.pdf` | 文字提取 |
| Word | `.docx` | 文字提取 |

---

## 💡 設計理念

### 零依賴架構

DocuMind 完全基於 Python 標準庫構建：
- **PDF 解析**: 自定義二進位制解析器，無需 PyPDF2
- **DOCX 解析**: ZIP/XML 解析器，無需 python-docx
- **文字分析**: 自定義 TF-IDF，無需 scikit-learn
- **TUI**: ANSI 轉義碼，無需 rich/curses

### 效能最佳化

- 大檔案流式處理
- 記憶體高效的文字分析
- 支援並行處理（未來）

---

## 📦 打包與部署

### 構建可執行檔案

```bash
# 安裝 PyInstaller
pip install pyinstaller

# 構建獨立可執行檔案
pyinstaller --onefile --name documind documind.py
```

### 作為包安裝

```bash
pip install -e .

# 然後全域性使用
documind document.pdf
```

---

## 🤝 貢獻指南

我們歡迎貢獻！請遵循以下準則：

1. Fork 倉庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟 Pull Request

### 提交資訊規範

- `feat:` 新功能
- `fix:` Bug 修復
- `docs:` 文件更改
- `refactor:` 程式碼重構
- `test:` 測試更改
- `chore:` 構建/工具更改

---

## 📄 開源協議

本專案採用 MIT 協議 - 檢視 [LICENSE](LICENSE) 檔案瞭解詳情。

---

<div align="center">

**Made with ❤️ by the DocuMind Team**

[⭐ Star us on GitHub](https://github.com/gitstq/DocuMind) | [🐛 Report Bug](https://github.com/gitstq/DocuMind/issues) | [💡 Request Feature](https://github.com/gitstq/DocuMind/issues)

</div>
