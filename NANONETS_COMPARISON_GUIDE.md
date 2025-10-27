# Nanonets vs PaddleOCR Comparison Guide

This guide explains how to use the benchmark tools to compare PaddleOCR with Nanonets OCR.

## Overview

The comparison workflow consists of three main steps:

1. **Analyze PDF** (Optional) - Identify complex pages automatically
2. **Extract Pages** - Convert PDF pages to images
3. **Benchmark** - Run PaddleOCR and collect performance metrics

## Prerequisites

### Install Dependencies

```bash
# Install PDF processing dependencies
pip install -r requirements_pdf.txt

# Or install individually
pip install PyMuPDF>=1.23.0 psutil>=5.9.0 Pillow>=10.0.0
```

### Verify PaddleOCR Installation

```bash
python quick_test.py
```

## Step-by-Step Workflow

### Step 1: Analyze PDF Complexity (Optional but Recommended)

The complexity analyzer scans your PDF and recommends the most challenging pages for testing:

```bash
python analyze_pdf_complexity.py test_documents/CIS_IBM_Cloud_Foundations_Benchmark_v1.1.0.pdf
```

**Options:**
- `--top 15` - Show top 15 most complex pages (default: 10)
- `--min-complexity 40` - Set minimum complexity threshold (default: 30)
- `--verbose` - Show detailed statistics

**Example output:**
```
Recommended Test Pages (Most Complex)
======================================================================
 Page |  Score | Blocks |     Text | Table  | Small Text
----------------------------------------------------------------------
    45 |   85.3 |     42 |     4521 | Yes    |        Yes
    67 |   78.2 |     38 |     3892 | Yes    |        Yes
    89 |   72.1 |     35 |     4102 | Yes    |         No
```

The tool suggests which pages to extract:
```
Page numbers: 45,67,89,102-105,125
```

### Step 2: Extract PDF Pages

Extract the recommended (or your chosen) pages from the PDF:

```bash
# Extract recommended pages
python extract_pdf_pages.py test_documents/CIS_IBM_Cloud_Foundations_Benchmark_v1.1.0.pdf --pages "45,67,89,102-105,125"

# Or extract specific pages manually
python extract_pdf_pages.py test_documents/CIS_IBM_Cloud_Foundations_Benchmark_v1.1.0.pdf --pages "10,25,50"
```

**Options:**
- `--pages "5,12,23-25,45"` - Page numbers to extract (required)
- `--output path/to/output` - Output directory (default: `test_documents/nanonets_comparison`)
- `--dpi 600` - Image resolution (default: 300)
- `--format jpg` - Output format: png or jpg (default: png)
- `--info` - Show PDF information without extracting

**Example output:**
```
PDF has 298 pages
Extracting pages at 300 DPI...
======================================================================
✓ Page  45 → page_045.png (2480x3508px, 1234.5 KB)
✓ Page  67 → page_067.png (2480x3508px, 1456.7 KB)
✓ Page  89 → page_089.png (2480x3508px, 1389.2 KB)
======================================================================
✓ Successfully extracted 3 pages
```

### Step 3: Run PaddleOCR Benchmark

Run the benchmark on all extracted pages:

```bash
python benchmark_nanonets_comparison.py
```

**Options:**
- `--input path/to/images` - Input directory (default: `test_documents/nanonets_comparison`)
- `--output path/to/results` - Output directory (default: `test_results/nanonets_comparison`)

**What it does:**
- Processes each extracted page with PaddleOCR
- Tracks detailed performance metrics:
  - Processing time (milliseconds)
  - Memory usage (MB)
  - Text regions detected
  - Confidence scores
  - Character count
- Generates multiple output formats

### Step 4: Review Results

The benchmark generates several output files in `test_results/nanonets_comparison/`:

#### Generated Files

**Summary Reports:**
- `nanonets_comparison_results.json` - Complete results with all metrics (for API comparison)
- `NANONETS_COMPARISON_REPORT.md` - Human-readable comparison report
- `performance_metrics.csv` - Spreadsheet-ready metrics

**Per-Page Results:**
- `page_045.json` - Structured OCR results with coordinates
- `page_045.txt` - Plain text extraction
- `page_045_annotated.jpg` - Visual output with bounding boxes

## Sharing with Colleagues

### Option 1: Share Everything

Send your colleagues:
1. The extracted page images from `test_documents/nanonets_comparison/`
2. The benchmark report: `NANONETS_COMPARISON_REPORT.md`

### Option 2: Share for Nanonets Testing

Send just the extracted pages:
```
test_documents/nanonets_comparison/
├── page_045.png
├── page_067.png
├── page_089.png
└── ...
```

They can run these through Nanonets and fill in the comparison table.

## Understanding the Results

### Metrics Explained

**Accuracy Metrics:**
- **Text Regions**: Number of text blocks detected
- **Total Characters**: Number of characters extracted
- **Average Confidence**: Mean confidence score (0.0 to 1.0)
- **Confidence Distribution**: 
  - High (≥0.9): Very confident predictions
  - Medium (0.7-0.9): Moderately confident
  - Low (<0.7): Less confident

**Performance Metrics:**
- **Processing Time**: Time to process each page
- **Peak Memory**: Maximum RAM used during processing
- **Average Time per Page**: Mean processing time

### Sample Comparison Report

The generated markdown report includes a comparison template:

```markdown
| Metric | PaddleOCR | Nanonets | Winner |
|--------|-----------|----------|--------|
| Total Processing Time (s) | 12.45 | [Add result] | |
| Avg Time per Page (ms) | 1556.25 | [Add result] | |
| Avg Confidence Score | 0.9234 | [Add result] | |
| Total Text Regions | 342 | [Add result] | |
| Total Characters | 28,456 | [Add result] | |
```

## Advanced Usage

### Custom Page Selection

Select pages based on specific criteria:

**Pages with tables:**
```bash
# Analyze first, then extract pages marked with "Table: Yes"
python analyze_pdf_complexity.py document.pdf --verbose
python extract_pdf_pages.py document.pdf --pages "23,45,67,89"
```

**High-resolution extraction:**
```bash
# Extract at 600 DPI for better quality
python extract_pdf_pages.py document.pdf --pages "10-15" --dpi 600
```

### Batch Testing Multiple PDFs

Process multiple documents:

```bash
# Extract pages from first PDF
python extract_pdf_pages.py doc1.pdf --pages "10,20,30" --output test_documents/comparison_batch1

# Extract pages from second PDF  
python extract_pdf_pages.py doc2.pdf --pages "5,15,25" --output test_documents/comparison_batch2

# Run benchmark on each
python benchmark_nanonets_comparison.py --input test_documents/comparison_batch1 --output test_results/batch1
python benchmark_nanonets_comparison.py --input test_documents/comparison_batch2 --output test_results/batch2
```

## Tips for Fair Comparison

1. **Use the same pages**: Ensure both systems process identical images
2. **Same resolution**: Use consistent DPI (300 recommended)
3. **Document complexity**: Include mix of simple and complex pages
4. **Multiple runs**: Run each system multiple times and average results
5. **Same hardware**: Test on the same machine for fair performance comparison

## Troubleshooting

### PDF Extraction Issues

**Problem**: "Error opening PDF"
```bash
# Check file exists
ls -l test_documents/CIS_IBM_Cloud_Foundations_Benchmark_v1.1.0.pdf

# Try with --info to see PDF details
python extract_pdf_pages.py document.pdf --info
```

**Problem**: "Page X does not exist"
```bash
# Check total pages first
python extract_pdf_pages.py document.pdf --info
```

### Benchmark Issues

**Problem**: "No images found"
```bash
# Verify images were extracted
ls test_documents/nanonets_comparison/

# Specify custom input directory
python benchmark_nanonets_comparison.py --input path/to/images
```

**Problem**: "PaddleOCR initialization failed"
```bash
# Test PaddleOCR first
python quick_test.py

# Reinstall if needed
pip install paddleocr[all]
```

## Example Complete Workflow

Here's a complete example from start to finish:

```bash
# 1. Analyze PDF to find complex pages
python analyze_pdf_complexity.py test_documents/CIS_IBM_Cloud_Foundations_Benchmark_v1.1.0.pdf --top 10

# Output suggests: pages 3,52,58,117,138,143,183,228,229,255

# 2. Extract those pages
python extract_pdf_pages.py test_documents/CIS_IBM_Cloud_Foundations_Benchmark_v1.1.0.pdf \
  --pages "3,52,58,117,138,143,183,228,229,255"

# 3. Run benchmark
python benchmark_nanonets_comparison.py

# 4. Review results
cat test_results/nanonets_comparison/NANONETS_COMPARISON_REPORT.md

# 5. Share extracted images with colleagues
# Send files from: test_documents/nanonets_comparison/
```

## Output Structure

```
test_documents/nanonets_comparison/
├── page_045.png
├── page_067.png
├── page_089.png
└── ...

test_results/nanonets_comparison/
├── nanonets_comparison_results.json    # Complete results (JSON)
├── NANONETS_COMPARISON_REPORT.md       # Markdown report
├── performance_metrics.csv             # CSV export
├── page_045.json                       # Per-page JSON
├── page_045.txt                        # Per-page text
├── page_045_annotated.jpg              # Per-page visualization
└── ...
```

