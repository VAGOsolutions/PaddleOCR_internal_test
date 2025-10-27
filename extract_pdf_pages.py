"""
PDF Page Extraction Tool
Extract specific pages from a PDF and convert them to high-quality images for OCR testing
"""

import os
import sys
import argparse
from pathlib import Path

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


def parse_page_numbers(page_string):
    """
    Parse page number string (e.g., "5,12,23-25,45") into list of page numbers
    
    Args:
        page_string: String with comma-separated page numbers and ranges
        
    Returns:
        List of page numbers (0-indexed)
    """
    pages = []
    parts = page_string.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            # Handle range (e.g., "23-25")
            start, end = part.split('-')
            start, end = int(start.strip()), int(end.strip())
            pages.extend(range(start, end + 1))
        else:
            # Single page number
            pages.append(int(part))
    
    # Convert to 0-indexed and remove duplicates
    pages = sorted(set(p - 1 for p in pages))
    return pages


def extract_pdf_pages(pdf_path, pages, output_dir, dpi=300, image_format='png'):
    """
    Extract specific pages from PDF and save as images
    
    Args:
        pdf_path: Path to input PDF file
        pages: List of page numbers to extract (0-indexed)
        output_dir: Directory to save extracted images
        dpi: Resolution for image extraction (default: 300)
        image_format: Output format ('png' or 'jpg')
        
    Returns:
        List of extracted image paths
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Open PDF
    try:
        pdf_document = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return []
    
    total_pages = pdf_document.page_count
    print(f"PDF has {total_pages} pages")
    
    extracted_files = []
    
    # Calculate zoom factor for desired DPI
    # Default is 72 DPI, so zoom = dpi / 72
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)
    
    print(f"\nExtracting pages at {dpi} DPI...")
    print("="*70)
    
    for page_idx in pages:
        if page_idx >= total_pages:
            print(f"Warning: Page {page_idx + 1} does not exist (PDF has {total_pages} pages)")
            continue
        
        try:
            # Load page
            page = pdf_document[page_idx]
            
            # Render page to image
            pix = page.get_pixmap(matrix=matrix)
            
            # Generate output filename
            page_num_str = f"{page_idx + 1:03d}"
            output_filename = f"page_{page_num_str}.{image_format}"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save image
            if image_format.lower() == 'png':
                pix.save(output_path)
            elif image_format.lower() in ['jpg', 'jpeg']:
                pix.save(output_path, output="jpeg")
            else:
                pix.save(output_path)
            
            # Get page info
            page_size = page.rect
            file_size = os.path.getsize(output_path) / 1024  # KB
            
            print(f"✓ Page {page_idx + 1:3d} → {output_filename} "
                  f"({pix.width}x{pix.height}px, {file_size:.1f} KB)")
            
            extracted_files.append(output_path)
            
        except Exception as e:
            print(f"✗ Error extracting page {page_idx + 1}: {e}")
    
    pdf_document.close()
    
    print("="*70)
    print(f"\n✓ Successfully extracted {len(extracted_files)} pages")
    print(f"Output directory: {output_dir}")
    
    return extracted_files


def analyze_pdf_info(pdf_path):
    """Display basic PDF information"""
    try:
        pdf_document = fitz.open(pdf_path)
        
        print("\n" + "="*70)
        print("PDF Information")
        print("="*70)
        print(f"File: {os.path.basename(pdf_path)}")
        print(f"Total Pages: {pdf_document.page_count}")
        print(f"File Size: {os.path.getsize(pdf_path) / (1024*1024):.2f} MB")
        
        # Get metadata
        metadata = pdf_document.metadata
        if metadata:
            print("\nMetadata:")
            for key, value in metadata.items():
                if value:
                    print(f"  {key}: {value}")
        
        # Sample first page dimensions
        if pdf_document.page_count > 0:
            first_page = pdf_document[0]
            print(f"\nPage Dimensions: {first_page.rect.width:.1f} x {first_page.rect.height:.1f} pts")
        
        pdf_document.close()
        print("="*70)
        
    except Exception as e:
        print(f"Error reading PDF: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract specific pages from a PDF for OCR testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract single page
  python extract_pdf_pages.py document.pdf --pages 5
  
  # Extract multiple pages
  python extract_pdf_pages.py document.pdf --pages "5,12,45"
  
  # Extract page ranges
  python extract_pdf_pages.py document.pdf --pages "10,23-25,45-47,89"
  
  # Show PDF info without extracting
  python extract_pdf_pages.py document.pdf --info
  
  # High resolution extraction (600 DPI)
  python extract_pdf_pages.py document.pdf --pages "5,10" --dpi 600
        """
    )
    
    parser.add_argument('pdf_file', help='Path to PDF file')
    parser.add_argument('--pages', '-p', help='Page numbers to extract (e.g., "5,12,23-25,45")')
    parser.add_argument('--output', '-o', default='test_documents/nanonets_comparison',
                        help='Output directory (default: test_documents/nanonets_comparison)')
    parser.add_argument('--dpi', type=int, default=300,
                        help='Image resolution in DPI (default: 300)')
    parser.add_argument('--format', choices=['png', 'jpg', 'jpeg'], default='png',
                        help='Output image format (default: png)')
    parser.add_argument('--info', action='store_true',
                        help='Show PDF information and exit')
    
    args = parser.parse_args()
    
    # Check if PDF exists
    if not os.path.exists(args.pdf_file):
        print(f"Error: PDF file not found: {args.pdf_file}")
        sys.exit(1)
    
    # Show info and exit if requested
    if args.info:
        analyze_pdf_info(args.pdf_file)
        return
    
    # Check if pages are specified
    if not args.pages:
        print("Error: Please specify pages to extract using --pages")
        print("\nExample: python extract_pdf_pages.py document.pdf --pages \"5,10,23-25\"")
        print("Or use --info to see PDF information")
        sys.exit(1)
    
    # Parse page numbers
    try:
        pages = parse_page_numbers(args.pages)
    except ValueError as e:
        print(f"Error parsing page numbers: {e}")
        print("Use format like: 5,12,23-25,45")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("PDF Page Extraction Tool")
    print("="*70)
    print(f"Input PDF: {args.pdf_file}")
    print(f"Pages to extract: {args.pages}")
    print(f"Parsed as: {sorted([p + 1 for p in pages])}")
    print(f"Resolution: {args.dpi} DPI")
    print(f"Format: {args.format.upper()}")
    
    # Extract pages
    extracted_files = extract_pdf_pages(
        args.pdf_file,
        pages,
        args.output,
        dpi=args.dpi,
        image_format=args.format
    )
    
    if extracted_files:
        print(f"\n✓ Ready for OCR testing!")
        print(f"\nNext step:")
        print(f"  python benchmark_nanonets_comparison.py")


if __name__ == "__main__":
    main()

