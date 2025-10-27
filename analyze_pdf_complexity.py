"""
PDF Complexity Analyzer
Analyzes a PDF to identify complex pages suitable for OCR benchmarking
"""

import os
import sys
import argparse
from collections import defaultdict

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')
    except Exception:
        pass

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF is not installed.")
    print("Please install it using: pip install PyMuPDF")
    sys.exit(1)


def analyze_page_complexity(page):
    """
    Analyze complexity of a single PDF page
    
    Args:
        page: PyMuPDF page object
        
    Returns:
        Dictionary with complexity metrics
    """
    complexity = {
        "text_blocks": 0,
        "text_length": 0,
        "images": 0,
        "tables_likely": False,
        "has_small_text": False,
        "text_density": 0,
        "complexity_score": 0
    }
    
    # Get text blocks
    blocks = page.get_text("dict")["blocks"]
    
    text_blocks = []
    image_count = 0
    total_text_length = 0
    font_sizes = []
    
    for block in blocks:
        if block["type"] == 0:  # Text block
            text_blocks.append(block)
            
            # Analyze text within block
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "")
                    total_text_length += len(text)
                    font_sizes.append(span.get("size", 12))
        
        elif block["type"] == 1:  # Image block
            image_count += 1
    
    complexity["text_blocks"] = len(text_blocks)
    complexity["text_length"] = total_text_length
    complexity["images"] = image_count
    
    # Check for small text (technical documents often have small fonts)
    if font_sizes:
        avg_font_size = sum(font_sizes) / len(font_sizes)
        min_font_size = min(font_sizes)
        complexity["avg_font_size"] = round(avg_font_size, 1)
        complexity["min_font_size"] = round(min_font_size, 1)
        
        if min_font_size < 8 or avg_font_size < 10:
            complexity["has_small_text"] = True
    
    # Detect tables (heuristic: multiple blocks in grid pattern)
    # Check if there are many blocks with similar vertical positions
    if len(text_blocks) >= 10:
        y_positions = defaultdict(int)
        for block in text_blocks:
            y = int(block["bbox"][1] / 10) * 10  # Group by 10pt intervals
            y_positions[y] += 1
        
        # If multiple rows have multiple columns, likely a table
        rows_with_multiple_items = sum(1 for count in y_positions.values() if count >= 3)
        if rows_with_multiple_items >= 3:
            complexity["tables_likely"] = True
    
    # Calculate text density (text length vs page area)
    page_area = page.rect.width * page.rect.height
    if page_area > 0:
        complexity["text_density"] = round(total_text_length / page_area, 4)
    
    # Calculate overall complexity score
    score = 0
    
    # More text blocks = more complex
    score += min(len(text_blocks) / 5, 10)
    
    # High text density = more complex
    score += min(complexity["text_density"] * 100, 15)
    
    # Tables are complex
    if complexity["tables_likely"]:
        score += 20
    
    # Small text is challenging
    if complexity["has_small_text"]:
        score += 15
    
    # Images add complexity
    score += min(image_count * 5, 10)
    
    # Long text adds moderate complexity
    score += min(total_text_length / 1000, 10)
    
    complexity["complexity_score"] = round(score, 2)
    
    return complexity


def analyze_pdf(pdf_path, min_complexity=30, top_n=10):
    """
    Analyze all pages in a PDF and recommend test pages
    
    Args:
        pdf_path: Path to PDF file
        min_complexity: Minimum complexity score to consider
        top_n: Number of top complex pages to recommend
        
    Returns:
        List of recommended page numbers and analysis data
    """
    try:
        pdf_document = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return None
    
    total_pages = pdf_document.page_count
    
    print("\n" + "="*70)
    print("PDF Complexity Analysis")
    print("="*70)
    print(f"File: {os.path.basename(pdf_path)}")
    print(f"Total pages: {total_pages}")
    print(f"Analyzing complexity...")
    print("="*70 + "\n")
    
    page_analyses = []
    
    for page_num in range(total_pages):
        page = pdf_document[page_num]
        complexity = analyze_page_complexity(page)
        complexity["page_number"] = page_num + 1
        page_analyses.append(complexity)
        
        # Progress indicator
        if (page_num + 1) % 50 == 0:
            print(f"Analyzed {page_num + 1}/{total_pages} pages...")
    
    pdf_document.close()
    
    # Sort by complexity score
    page_analyses.sort(key=lambda x: x["complexity_score"], reverse=True)
    
    # Filter by minimum complexity
    complex_pages = [p for p in page_analyses if p["complexity_score"] >= min_complexity]
    
    # Get top N
    recommended_pages = complex_pages[:top_n]
    
    return {
        "total_pages": total_pages,
        "all_analyses": page_analyses,
        "complex_pages": complex_pages,
        "recommended_pages": recommended_pages
    }


def print_recommendations(analysis_data, verbose=False):
    """Print analysis results and recommendations"""
    
    recommended = analysis_data["recommended_pages"]
    
    print("\n" + "="*70)
    print("Recommended Test Pages (Most Complex)")
    print("="*70)
    print(f"Found {len(analysis_data['complex_pages'])} complex pages")
    print(f"Top {len(recommended)} recommendations:\n")
    
    print(f"{'Page':>6} | {'Score':>6} | {'Blocks':>7} | {'Text':>8} | {'Table':>6} | {'Small Text':>10}")
    print("-" * 70)
    
    for page_info in recommended:
        print(f"{page_info['page_number']:6d} | "
              f"{page_info['complexity_score']:6.1f} | "
              f"{page_info['text_blocks']:7d} | "
              f"{page_info['text_length']:8d} | "
              f"{'Yes' if page_info['tables_likely'] else 'No':6s} | "
              f"{'Yes' if page_info['has_small_text'] else 'No':>10s}")
    
    print("\n" + "="*70)
    print("Suggested Pages for Testing:")
    print("="*70)
    
    # Create page list string
    page_numbers = [str(p['page_number']) for p in recommended]
    
    # Group consecutive pages
    grouped = []
    i = 0
    while i < len(page_numbers):
        start = i
        while i + 1 < len(page_numbers) and int(page_numbers[i + 1]) == int(page_numbers[i]) + 1:
            i += 1
        
        if i > start + 1:
            grouped.append(f"{page_numbers[start]}-{page_numbers[i]}")
        else:
            grouped.append(page_numbers[start])
        i += 1
    
    pages_string = ",".join(grouped)
    
    print(f"\nPage numbers: {pages_string}\n")
    print("Run extraction command:")
    print(f"  python extract_pdf_pages.py \"{analysis_data['pdf_path']}\" --pages \"{pages_string}\"")
    print("\n" + "="*70)
    
    # Additional statistics
    if verbose:
        print("\nDetailed Statistics:")
        print("="*70)
        
        all_scores = [p["complexity_score"] for p in analysis_data["all_analyses"]]
        avg_score = sum(all_scores) / len(all_scores)
        
        table_count = sum(1 for p in analysis_data["all_analyses"] if p["tables_likely"])
        small_text_count = sum(1 for p in analysis_data["all_analyses"] if p["has_small_text"])
        
        print(f"Average complexity score: {avg_score:.2f}")
        print(f"Pages with likely tables: {table_count}")
        print(f"Pages with small text: {small_text_count}")
        print(f"Highest complexity score: {max(all_scores):.2f} (page {analysis_data['all_analyses'][0]['page_number']})")
        print(f"Lowest complexity score: {min(all_scores):.2f}")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze PDF complexity to identify good test pages for OCR benchmarking',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This tool analyzes each page of a PDF and scores it based on:
- Number of text blocks
- Text density
- Presence of tables
- Small font sizes
- Images
- Overall text length

Higher scores indicate more complex pages that are good candidates for OCR testing.

Example:
  python analyze_pdf_complexity.py document.pdf --top 15
        """
    )
    
    parser.add_argument('pdf_file', help='Path to PDF file')
    parser.add_argument('--top', '-t', type=int, default=10,
                        help='Number of top complex pages to recommend (default: 10)')
    parser.add_argument('--min-complexity', '-m', type=float, default=30,
                        help='Minimum complexity score threshold (default: 30)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed statistics')
    
    args = parser.parse_args()
    
    # Check if PDF exists
    if not os.path.exists(args.pdf_file):
        print(f"Error: PDF file not found: {args.pdf_file}")
        sys.exit(1)
    
    # Analyze PDF
    analysis_data = analyze_pdf(args.pdf_file, args.min_complexity, args.top)
    
    if analysis_data:
        analysis_data["pdf_path"] = args.pdf_file
        print_recommendations(analysis_data, args.verbose)
    else:
        print("Analysis failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()

