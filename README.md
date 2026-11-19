# PDF to Markdown Converter (Local & Privacy-First)

[English](README.md) | [繁體中文](README_zh.md)

A lightweight, high-performance, and privacy-preserving tool to convert PDF documents into clean, LLM-ready GitHub-Flavored Markdown (GFM).

Designed for individuals, researchers, and enterprises handling sensitive documents who want **100% offline processing**, **zero cloud API costs**, and **seamless Windows desktop integration**.

---

## Key Highlights

- **100% Local & Privacy-First**: Documents never leave your machine. No telemetry, no external network requests, and zero data leakage.
- **Zero API Costs**: No OpenAI, Anthropic, or cloud vision API keys required. All layout analysis and OCR run locally.
- **Automatic Offline OCR**: Scanned PDFs and raster images are recognized automatically using local ONNX models via RapidOCR.
- **LLM-Ready Markdown Structure**: Preserves hierarchical headers (`#`, `##`, `###`), tables (`| col | col |`), code blocks, bullet points, and multi-column reading flow.
- **Windows Explorer Context Menu**: Convert any PDF instantly by right-clicking it in Windows Explorer (`Convert to Markdown (.md)`).
- **Flexible CLI**: Convert single documents, specify custom outputs, or batch convert multiple files via standard terminal commands.

---

## System Architecture & Engine Comparison

| Feature | This Project (PyMuPDF4LLM + RapidOCR) | Cloud Multimodal APIs | Standard PDF Extractors |
| :--- | :--- | :--- | :--- |
| **Privacy & Security** | **100% Offline / Local** | Sends documents to cloud | Local |
| **Cost** | **$0.00 (Free)** | Per-token / per-image fees | $0.00 |
| **Scanned PDF (OCR)** | **Built-in ONNX OCR** | Supported (costly) | Usually fails / empty |
| **Table Formatting** | **Markdown Pipe Tables** | Markdown Tables | Raw unstructured text |
| **Heading Detection** | **Font-size hierarchy** | Inferred | Plain text |
| **Speed** | **Sub-second (~0.7s)** | 3-10s latency | Fast |

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Windows 10/11 (for context menu features; CLI works cross-platform)

### Setup
1. Clone or download this repository:
   ```bash
   git clone https://github.com/your-username/pdf-to-md.git
   cd pdf-to-md
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Windows Explorer Context Menu Setup

Convert any PDF with a single right-click in Windows Explorer:

### 1-Click Install
Double-click `install_context_menu.bat` or run:
```bash
python setup_context_menu.py --install
```

- **No Administrator Privileges Required**: Registers in `HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.pdf`.
- **Silent Background Execution**: Runs via `pythonw.exe`, so no intrusive command prompt window flashes on your screen.
- **Output Location**: Generates `<filename>.md` directly in the same folder as the right-clicked PDF.

### Uninstallation
Double-click `uninstall_context_menu.bat` or run:
```bash
python setup_context_menu.py --uninstall
```

---

## Command-Line Interface (CLI) Usage

### 1. Basic Conversion
Convert a PDF to Markdown in the same directory (`document.pdf` -> `document.md`):
```bash
python pdf_to_md.py document.pdf
```

### 2. Specify Output File
Specify an explicit output markdown file:
```bash
python pdf_to_md.py document.pdf output.md
# or using flag:
python pdf_to_md.py -o /path/to/custom_output.md document.pdf
```

### 3. Batch Conversion
Convert multiple PDF files in one command:
```bash
python pdf_to_md.py report1.pdf report2.pdf thesis.pdf
```

### 4. Extract Embedded Images
Extract embedded document images into a dedicated subfolder alongside the markdown file:
```bash
python pdf_to_md.py --extract-images report.pdf
```

### 5. CLI Options Reference

```text
usage: pdf_to_md.py [-h] [-o OUTPUT] [--engine {auto,pymupdf4llm,markitdown}]
                    [--extract-images] [-v] [-q] [--version]
                    [inputs ...]

positional arguments:
  inputs                Input PDF file(s).

options:
  -h, --help            Show help message and exit.
  -o, --output OUTPUT   Output markdown file path (single file mode).
  --engine {auto,pymupdf4llm,markitdown}
                        Engine preference (default: auto, prefers pymupdf4llm).
  --extract-images      Extract and save embedded images locally.
  -v, --verbose         Enable detailed logging output.
  -q, --quiet           Suppress non-error console output.
  --version             Show program's version number and exit.
```

---

## Quality & Edge-Case Engineering

- **RapidOCR NoneType Guard**: Upstream PyMuPDF4LLM 2.1 contains an issue where images without extractable text cause `TypeError: 'NoneType' object is not iterable`. This codebase includes an active runtime guard ensuring graceful handling of purely graphic/blank pages.
- **Smart Fallback**: If `pymupdf4llm` encounters an unhandled document exception, the tool automatically attempts fallback extraction through `markitdown`.
- **Silent Context Menu Error Logging**: If a background conversion invoked from File Explorer fails, an error traceback is written to `convert_error.log` in the target file's directory for easy troubleshooting.

---

## Project Structure

```text
.
├── pdf_to_md.py                # Main conversion script (CLI & context menu entrypoint)
├── setup_context_menu.py       # Context menu installer/uninstaller script
├── install_context_menu.bat    # 1-Click Windows context menu installer
├── uninstall_context_menu.bat  # 1-Click Windows context menu uninstaller
├── add_pdf_to_md_context.reg   # Generated registry file for context menu
├── remove_pdf_to_md_context.reg# Generated registry file to remove context menu
├── requirements.txt            # Dependency specification
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── README.md                   # Documentation (English)
└── README_zh.md                # Documentation (Traditional Chinese)
```

---

## License

This project is licensed under the [MIT License](LICENSE).
