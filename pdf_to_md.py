#!/usr/bin/env python3
"""
PDF to Markdown Converter (Local, Privacy-First, Zero API Cost)
Supports both command-line (CLI) usage and Windows right-click context menu execution.
"""

import os
import sys
import argparse
import logging
from typing import Optional, List

__version__ = "1.0.0"

# Setup logger
logger = logging.getLogger("pdf_to_md")


def patch_rapidocr_none_safety():
    """
    Guard against upstream pymupdf4llm bug where full_ocr() throws
    TypeError: 'NoneType' object is not iterable when an image has no text.
    """
    try:
        import pymupdf4llm.ocr.rapidocr_onnx_backend as ocr_backend

        def safe_full_ocr(img):
            engine = ocr_backend.init_engine()
            results, _ = engine(img)
            if results is None:
                return []
            return [(box, text, float(score)) for box, text, score in results]

        ocr_backend.full_ocr = safe_full_ocr
    except Exception:
        pass


def convert_with_pymupdf4llm(
    pdf_path: str,
    write_images: bool = False,
    image_path: Optional[str] = None
) -> str:
    """Convert PDF to Markdown using PyMuPDF4LLM with local OCR support."""
    patch_rapidocr_none_safety()
    import pymupdf4llm

    kwargs = {}
    if write_images:
        kwargs["write_images"] = True
        if image_path:
            kwargs["image_path"] = image_path

    try:
        content = pymupdf4llm.to_markdown(pdf_path, **kwargs)
        return content
    except TypeError as e:
        # If OCR fails on edge case, retry without image OCR
        logger.warning(f"OCR parsing exception: {e}. Retrying with plain text extraction...")
        import fitz
        doc = fitz.open(pdf_path)
        pages_text = [page.get_text() for page in doc]
        return "\n\n".join(pages_text)


def convert_with_markitdown(pdf_path: str) -> str:
    """Convert PDF to Markdown using MarkItDown."""
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(pdf_path)
    return result.text_content


def convert_pdf_to_md(
    pdf_path: str,
    output_path: Optional[str] = None,
    engine: str = "auto",
    write_images: bool = False
) -> str:
    """
    Convert a single PDF file to Markdown.

    :param pdf_path: Path to the input PDF file.
    :param output_path: Destination path for .md file. Defaults to same directory as PDF.
    :param engine: 'auto', 'pymupdf4llm', or 'markitdown'.
    :param write_images: Whether to extract and save images locally.
    :return: The converted markdown file path.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Input PDF not found: {pdf_path}")

    base_dir = os.path.dirname(os.path.abspath(pdf_path))
    file_stem = os.path.splitext(os.path.basename(pdf_path))[0]

    if not output_path:
        output_path = os.path.join(base_dir, f"{file_stem}.md")

    content = None
    errors = []

    # Engine selection logic
    engines_to_try = []
    if engine == "pymupdf4llm":
        engines_to_try = [("pymupdf4llm", convert_with_pymupdf4llm)]
    elif engine == "markitdown":
        engines_to_try = [("markitdown", convert_with_markitdown)]
    else:  # 'auto': prefer pymupdf4llm for high fidelity, OCR and tables
        engines_to_try = [
            ("pymupdf4llm", convert_with_pymupdf4llm),
            ("markitdown", convert_with_markitdown),
        ]

    for eng_name, eng_func in engines_to_try:
        try:
            logger.info(f"Attempting conversion using engine '{eng_name}'...")
            if eng_name == "pymupdf4llm":
                img_dir = os.path.join(base_dir, f"{file_stem}_images") if write_images else None
                content = eng_func(pdf_path, write_images=write_images, image_path=img_dir)
            else:
                content = eng_func(pdf_path)
            if content is not None:
                logger.info(f"Successfully converted using engine '{eng_name}'.")
                break
        except Exception as e:
            err_msg = f"Engine '{eng_name}' failed: {e}"
            logger.warning(err_msg)
            errors.append(err_msg)

    if content is None:
        combined_err = "All conversion engines failed.\n" + "\n".join(errors)
        raise RuntimeError(combined_err)

    # Ensure parent directory for output exists
    out_dir = os.path.dirname(os.path.abspath(output_path))
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"Markdown output saved to: {output_path}")
    return output_path


def log_context_error(pdf_path: str, err: Exception):
    """Write error log when running silently from Windows Explorer context menu."""
    try:
        base_dir = os.path.dirname(os.path.abspath(pdf_path)) if pdf_path else os.getcwd()
        error_log_path = os.path.join(base_dir, "convert_error.log")
        import traceback
        with open(error_log_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- Error converting {pdf_path} ---\n")
            f.write(f"Exception: {str(err)}\n")
            f.write(traceback.format_exc())
    except Exception:
        pass


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert PDF files to high-quality Markdown locally (100% offline, privacy-first)."
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Input PDF file(s). If run with one file and no -o, outputs to same directory as .md.",
    )
    parser.add_argument(
        "-o", "--output",
        dest="output",
        help="Output markdown file path (valid when converting a single PDF).",
    )
    parser.add_argument(
        "--engine",
        choices=["auto", "pymupdf4llm", "markitdown"],
        default="auto",
        help="Conversion engine to use (default: auto, prefers pymupdf4llm).",
    )
    parser.add_argument(
        "--extract-images",
        action="store_true",
        help="Extract and save embedded images to a local folder.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable detailed log output.",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress console output.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser.parse_args()


def main():
    # If no arguments given, show help and exit
    if len(sys.argv) == 1:
        # Check if stdin is a tty (terminal) or GUI invocation
        if sys.stdin and sys.stdin.isatty():
            parse_args_parser = argparse.ArgumentParser(
                description="Convert PDF files to Markdown locally."
            )
            parse_args_parser.print_help()
            sys.exit(0)
        else:
            sys.exit(0)

    # Context menu compatibility check:
    # If sys.argv has exactly 2 elements and sys.argv[1] is an existing PDF,
    # it might be called from Explorer or CLI positional: python pdf_to_md.py input.pdf [output.md]
    args = parse_args()

    # Configure logging
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    elif args.quiet:
        log_level = logging.ERROR

    logging.basicConfig(
        level=log_level,
        format="[%(levelname)s] %(message)s"
    )

    if not args.inputs:
        logger.error("No input PDF files provided. Use --help for usage information.")
        sys.exit(1)

    # Handle output argument constraint
    if args.output and len(args.inputs) > 1:
        logger.error("Error: -o/--output cannot be specified when converting multiple PDF files.")
        sys.exit(1)

    # Process files
    exit_code = 0
    for idx, input_pdf in enumerate(args.inputs):
        # Support positional second argument: python pdf_to_md.py input.pdf output.md
        target_output = args.output
        if not target_output and len(args.inputs) == 2 and args.inputs[1].lower().endswith(".md"):
            if idx == 0:
                target_output = args.inputs[1]
            else:
                break  # Already processed as target_output

        try:
            out_file = convert_pdf_to_md(
                pdf_path=input_pdf,
                output_path=target_output,
                engine=args.engine,
                write_images=args.extract_images
            )
            if not args.quiet:
                print(f"[+] Converted: {input_pdf} -> {out_file}")
        except Exception as e:
            exit_code = 1
            logger.error(f"Failed to convert '{input_pdf}': {e}")
            # If running in GUI/context menu mode (no tty stdout), write to error.log
            log_context_error(input_pdf, e)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
