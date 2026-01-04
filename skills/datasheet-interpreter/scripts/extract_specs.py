#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx",
#     "pdfplumber",
# ]
# ///
"""
Datasheet Spec Extractor - Extracts key specifications from component datasheet PDFs

Downloads datasheet PDFs from URLs and extracts:
- Voltage/current ratings
- Pin configurations  
- I2C/SPI addresses
- Operating temperature
- Timing parameters

Usage:
    uv run extract_specs.py --url "https://example.com/datasheet.pdf"
    uv run extract_specs.py --url "https://example.com/datasheet.pdf" --format markdown
    uv run extract_specs.py --file "local_datasheet.pdf"
    uv run extract_specs.py --interactive
"""

import argparse
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx
import pdfplumber


# =============================================================================
# Extraction Patterns - Regex for common datasheet parameters
# =============================================================================

PATTERNS = {
    # Voltage patterns
    "supply_voltage": [
        r"(?:VCC|VDD|Supply|Operating)\s*(?:Voltage)?[\s:=]+(\d+\.?\d*)\s*(?:to|[-–])\s*(\d+\.?\d*)\s*V",
        r"(\d+\.?\d*)\s*V\s*(?:to|[-–])\s*(\d+\.?\d*)\s*V\s*(?:supply|operating|input)",
        r"(?:Power Supply|Input Voltage)[\s:]+(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)\s*V",
    ],
    
    # Current patterns  
    "supply_current": [
        r"(?:Supply|Operating|Active)\s*Current[\s:=]+(\d+\.?\d*)\s*(mA|µA|uA|μA)",
        r"(?:ICC|IDD)[\s:=]+(\d+\.?\d*)\s*(mA|µA|uA|μA)",
        r"Current\s*Consumption[\s:=]+(\d+\.?\d*)\s*(mA|µA|uA|μA)",
    ],
    
    # Standby/Sleep current
    "standby_current": [
        r"(?:Standby|Sleep|Power.?Down)\s*(?:Current|Mode)?[\s:=]+(\d+\.?\d*)\s*(mA|µA|uA|μA|nA)",
        r"(?:ISB|ISBY)[\s:=]+(\d+\.?\d*)\s*(µA|uA|μA|nA)",
    ],
    
    # I2C Address
    "i2c_address": [
        r"(?:I2C|I²C|IIC)\s*(?:Address|Addr)[\s:=]*(0x[0-9A-Fa-f]{2})",
        r"(?:Slave|Device)\s*Address[\s:=]*(0x[0-9A-Fa-f]{2})",
        r"Address[\s:=]*(0x[0-9A-Fa-f]{2})\s*(?:\(7.?bit\))?",
        r"(0x[0-9A-Fa-f]{2})\s*(?:\(W\)|write|read)",
    ],
    
    # SPI Clock
    "spi_clock": [
        r"(?:SPI|SCLK|SCK)\s*(?:Clock|Frequency)?[\s:=]+(?:up to\s*)?(\d+\.?\d*)\s*(MHz|kHz)",
        r"(?:Serial Clock|fSCL)[\s:=]+(\d+\.?\d*)\s*(MHz|kHz)",
    ],
    
    # Operating Temperature
    "temperature_range": [
        r"(?:Operating|Ambient)\s*Temperature[\s:=]*([-]?\d+)\s*°?C?\s*(?:to|[-–])\s*([-]?\d+)\s*°?C",
        r"(?:TA|TOPR)[\s:=]*([-]?\d+)\s*(?:to|[-–])\s*([-]?\d+)\s*°?C",
        r"([-]?\d+)\s*°C\s*to\s*([-]?\d+)\s*°C\s*(?:operating|ambient)",
    ],
    
    # Resolution (for ADCs, sensors)
    "resolution": [
        r"(?:Resolution|ADC)[\s:=]+(\d+)\s*(?:-)?bit",
        r"(\d+)\s*(?:-)?bit\s*(?:resolution|ADC|DAC)",
    ],
    
    # Package/Pins
    "package": [
        r"(?:Package|Pkg)[\s:=]+(\w+[-]?\d+)",
        r"(SO(?:IC)?[-]?\d+|DIP[-]?\d+|QFN[-]?\d+|TQFP[-]?\d+|BGA[-]?\d+)",
    ],
    
    # Accuracy (for sensors)
    "accuracy": [
        r"(?:Accuracy|Typical Accuracy)[\s:=]+[±]?(\d+\.?\d*)\s*(%|°C|°|LSB)",
        r"[±](\d+\.?\d*)\s*(%|°C)\s*(?:accuracy|typical)",
    ],
}


@dataclass
class ExtractedSpecs:
    """Container for extracted specifications"""
    source: str
    supply_voltage: Optional[str] = None
    supply_current: Optional[str] = None
    standby_current: Optional[str] = None
    i2c_addresses: list = field(default_factory=list)
    spi_clock: Optional[str] = None
    temperature_range: Optional[str] = None
    resolution: Optional[str] = None
    package: Optional[str] = None
    accuracy: Optional[str] = None
    raw_text_sample: str = ""
    tables: list = field(default_factory=list)


def download_pdf(url: str, timeout: float = 30.0) -> bytes:
    """Download PDF from URL with progress indication"""
    print(f"Downloading: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    with httpx.Client(follow_redirects=True, timeout=timeout) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        
        content_type = response.headers.get("content-type", "")
        if "pdf" not in content_type.lower() and not url.lower().endswith(".pdf"):
            print(f"Warning: Content-Type is '{content_type}', may not be a PDF")
        
        print(f"Downloaded: {len(response.content):,} bytes")
        return response.content


def extract_text_from_pdf(pdf_path: Path, max_pages: int = 20) -> tuple[str, list]:
    """Extract text and tables from PDF"""
    all_text = []
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        page_count = min(len(pdf.pages), max_pages)
        print(f"Processing {page_count} pages...")
        
        for i, page in enumerate(pdf.pages[:max_pages]):
            # Extract text
            text = page.extract_text() or ""
            all_text.append(text)
            
            # Extract tables (first 5 pages only - usually contain specs)
            if i < 5:
                tables = page.extract_tables()
                for table in tables:
                    if table and len(table) > 1:  # Has header + data
                        all_tables.append(table)
    
    return "\n".join(all_text), all_tables


def extract_specs(text: str, tables: list, source: str) -> ExtractedSpecs:
    """Extract specifications using regex patterns"""
    specs = ExtractedSpecs(source=source)
    
    # Normalize text for better matching
    text_normalized = text.replace('\n', ' ').replace('  ', ' ')
    
    # Extract voltage
    for pattern in PATTERNS["supply_voltage"]:
        match = re.search(pattern, text_normalized, re.IGNORECASE)
        if match:
            specs.supply_voltage = f"{match.group(1)}-{match.group(2)}V"
            break
    
    # Extract supply current
    for pattern in PATTERNS["supply_current"]:
        match = re.search(pattern, text_normalized, re.IGNORECASE)
        if match:
            specs.supply_current = f"{match.group(1)} {match.group(2)}"
            break
    
    # Extract standby current
    for pattern in PATTERNS["standby_current"]:
        match = re.search(pattern, text_normalized, re.IGNORECASE)
        if match:
            specs.standby_current = f"{match.group(1)} {match.group(2)}"
            break
    
    # Extract I2C addresses (can have multiple)
    for pattern in PATTERNS["i2c_address"]:
        matches = re.findall(pattern, text_normalized, re.IGNORECASE)
        for addr in matches:
            if addr not in specs.i2c_addresses:
                specs.i2c_addresses.append(addr)
    
    # Extract SPI clock
    for pattern in PATTERNS["spi_clock"]:
        match = re.search(pattern, text_normalized, re.IGNORECASE)
        if match:
            specs.spi_clock = f"{match.group(1)} {match.group(2)}"
            break
    
    # Extract temperature range
    for pattern in PATTERNS["temperature_range"]:
        match = re.search(pattern, text_normalized, re.IGNORECASE)
        if match:
            specs.temperature_range = f"{match.group(1)}°C to {match.group(2)}°C"
            break
    
    # Extract resolution
    for pattern in PATTERNS["resolution"]:
        match = re.search(pattern, text_normalized, re.IGNORECASE)
        if match:
            specs.resolution = f"{match.group(1)}-bit"
            break
    
    # Extract package
    for pattern in PATTERNS["package"]:
        match = re.search(pattern, text_normalized, re.IGNORECASE)
        if match:
            specs.package = match.group(1)
            break
    
    # Extract accuracy
    for pattern in PATTERNS["accuracy"]:
        match = re.search(pattern, text_normalized, re.IGNORECASE)
        if match:
            specs.accuracy = f"±{match.group(1)}{match.group(2)}"
            break
    
    # Store raw text sample (first 500 chars for context)
    specs.raw_text_sample = text[:500].strip()
    
    # Store relevant tables
    specs.tables = tables[:3]  # First 3 tables
    
    return specs


def format_text(specs: ExtractedSpecs) -> str:
    """Format extracted specs as plain text"""
    lines = [
        "=" * 60,
        "  DATASHEET SPEC EXTRACTION",
        "=" * 60,
        "",
        f"Source: {specs.source}",
        "",
        "EXTRACTED SPECIFICATIONS:",
        "-" * 40,
    ]
    
    if specs.supply_voltage:
        lines.append(f"  Supply Voltage:    {specs.supply_voltage}")
    if specs.supply_current:
        lines.append(f"  Supply Current:    {specs.supply_current}")
    if specs.standby_current:
        lines.append(f"  Standby Current:   {specs.standby_current}")
    if specs.i2c_addresses:
        lines.append(f"  I2C Address(es):   {', '.join(specs.i2c_addresses)}")
    if specs.spi_clock:
        lines.append(f"  SPI Clock:         {specs.spi_clock}")
    if specs.temperature_range:
        lines.append(f"  Temperature:       {specs.temperature_range}")
    if specs.resolution:
        lines.append(f"  Resolution:        {specs.resolution}")
    if specs.package:
        lines.append(f"  Package:           {specs.package}")
    if specs.accuracy:
        lines.append(f"  Accuracy:          {specs.accuracy}")
    
    # Check if nothing was extracted
    has_specs = any([
        specs.supply_voltage, specs.supply_current, specs.standby_current,
        specs.i2c_addresses, specs.spi_clock, specs.temperature_range,
        specs.resolution, specs.package, specs.accuracy
    ])
    
    if not has_specs:
        lines.append("  (No specifications auto-extracted)")
        lines.append("  Try reading the datasheet manually for specs")
    
    lines.append("")
    
    # Show tables if found
    if specs.tables:
        lines.append("SPECIFICATION TABLES FOUND:")
        lines.append("-" * 40)
        for i, table in enumerate(specs.tables[:2], 1):
            lines.append(f"\nTable {i}:")
            for row in table[:5]:  # First 5 rows
                if row:
                    lines.append("  " + " | ".join(str(cell or "")[:20] for cell in row))
            if len(table) > 5:
                lines.append(f"  ... ({len(table) - 5} more rows)")
    
    lines.append("")
    lines.append("RAW TEXT SAMPLE (first 300 chars):")
    lines.append("-" * 40)
    lines.append(specs.raw_text_sample[:300])
    
    return "\n".join(lines)


def format_markdown(specs: ExtractedSpecs) -> str:
    """Format extracted specs as markdown"""
    lines = [
        "# Datasheet Specification Extract",
        "",
        f"**Source:** `{specs.source}`",
        "",
        "## Extracted Specifications",
        "",
        "| Parameter | Value |",
        "|-----------|-------|",
    ]
    
    if specs.supply_voltage:
        lines.append(f"| Supply Voltage | {specs.supply_voltage} |")
    if specs.supply_current:
        lines.append(f"| Supply Current | {specs.supply_current} |")
    if specs.standby_current:
        lines.append(f"| Standby Current | {specs.standby_current} |")
    if specs.i2c_addresses:
        lines.append(f"| I2C Address | {', '.join(specs.i2c_addresses)} |")
    if specs.spi_clock:
        lines.append(f"| SPI Clock | {specs.spi_clock} |")
    if specs.temperature_range:
        lines.append(f"| Operating Temp | {specs.temperature_range} |")
    if specs.resolution:
        lines.append(f"| Resolution | {specs.resolution} |")
    if specs.package:
        lines.append(f"| Package | {specs.package} |")
    if specs.accuracy:
        lines.append(f"| Accuracy | {specs.accuracy} |")
    
    lines.append("")
    
    # Tables
    if specs.tables:
        lines.append("## Specification Tables")
        lines.append("")
        for i, table in enumerate(specs.tables[:2], 1):
            lines.append(f"### Table {i}")
            lines.append("")
            # Convert to markdown table
            if table and len(table) > 0:
                header = table[0]
                lines.append("| " + " | ".join(str(h or "")[:20] for h in header) + " |")
                lines.append("| " + " | ".join(["---"] * len(header)) + " |")
                for row in table[1:6]:
                    lines.append("| " + " | ".join(str(c or "")[:20] for c in row) + " |")
                if len(table) > 6:
                    lines.append(f"*... {len(table) - 6} more rows*")
            lines.append("")
    
    return "\n".join(lines)


def process_url(url: str, output_format: str = "text") -> str:
    """Main processing function for URL input"""
    try:
        # Download PDF
        pdf_bytes = download_pdf(url)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(pdf_bytes)
            tmp_path = Path(tmp.name)
        
        try:
            # Extract text and tables
            text, tables = extract_text_from_pdf(tmp_path)
            
            # Extract specs
            specs = extract_specs(text, tables, url)
            
            # Format output
            if output_format == "markdown":
                return format_markdown(specs)
            else:
                return format_text(specs)
        finally:
            # Cleanup temp file
            tmp_path.unlink(missing_ok=True)
            
    except httpx.HTTPError as e:
        return f"Error downloading PDF: {e}"
    except Exception as e:
        return f"Error processing PDF: {e}"


def process_file(file_path: str, output_format: str = "text") -> str:
    """Process local PDF file"""
    path = Path(file_path)
    if not path.exists():
        return f"Error: File not found: {file_path}"
    
    try:
        text, tables = extract_text_from_pdf(path)
        specs = extract_specs(text, tables, str(path))
        
        if output_format == "markdown":
            return format_markdown(specs)
        else:
            return format_text(specs)
    except Exception as e:
        return f"Error processing PDF: {e}"


def interactive_mode():
    """Interactive mode for spec extraction"""
    print("=" * 60)
    print("Datasheet Spec Extractor - Interactive Mode")
    print("=" * 60)
    print()
    print("Enter a datasheet PDF URL or local file path")
    print("Type 'quit' or 'q' to exit")
    print()
    
    while True:
        source = input("PDF URL or path> ").strip()
        
        if not source:
            continue
        if source.lower() in ['quit', 'exit', 'q']:
            break
        
        print()
        
        if source.startswith(('http://', 'https://')):
            result = process_url(source)
        else:
            result = process_file(source)
        
        print(result)
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Extract specifications from component datasheet PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run extract_specs.py --url "https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf"
  uv run extract_specs.py --url "https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf" --format markdown
  uv run extract_specs.py --file "local_datasheet.pdf"
  uv run extract_specs.py --interactive
        """
    )
    parser.add_argument("--url", "-u", type=str, help="URL of datasheet PDF to download and extract")
    parser.add_argument("--file", "-f", type=str, help="Local PDF file path")
    parser.add_argument("--format", type=str, default="text", 
                        choices=["text", "markdown"], help="Output format")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
        return
    
    if args.url:
        result = process_url(args.url, args.format)
        print(result)
        return
    
    if args.file:
        result = process_file(args.file, args.format)
        print(result)
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
