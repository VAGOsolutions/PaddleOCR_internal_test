"""
Page to Markdown Converter
Convert multiple document page images to structured Markdown files using PP-StructureV3
"""

import os
import sys
import argparse
import time
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
    from paddleocr import PPStructureV3
except ImportError:
    print("Error: PaddleOCR is not installed.")
    print("Please install it using: pip install \"paddleocr[all]\"")
    sys.exit(1)


def get_image_files(input_dir):
    """
    Get all image files from input directory
    
    Args:
        input_dir: Path to directory containing images
        
    Returns:
        Sorted list of image file paths
    """
    supported_formats = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"Error: Input directory does not exist: {input_dir}")
        return []
    
    if not input_path.is_dir():
        print(f"Error: Input path is not a directory: {input_dir}")
        return []
    
    # Find all image files
    image_files = []
    for file_path in input_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_formats:
            image_files.append(file_path)
    
    # Sort files naturally (page_001.png, page_002.png, etc.)
    image_files.sort(key=lambda x: x.name)
    
    return image_files


def convert_pages_to_markdown(input_dir, output_dir, show_progress=True):
    """
    Convert all page images in input directory to markdown files
    
    Args:
        input_dir: Directory containing page images
        output_dir: Directory to save markdown files
        show_progress: Whether to show progress messages
        
    Returns:
        Dictionary with conversion statistics
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get image files
    image_files = get_image_files(input_dir)
    
    if not image_files:
        print(f"No image files found in: {input_dir}")
        return {'success': 0, 'failed': 0, 'total': 0}
    
    print(f"Found {len(image_files)} image files to process")
    print("="*70)
    
    # Initialize PP-StructureV3
    if show_progress:
        print("\nInitializing PP-StructureV3...")
    
    try:
        pipeline = PPStructureV3()
    except Exception as e:
        print(f"Error initializing PP-StructureV3: {e}")
        return {'success': 0, 'failed': len(image_files), 'total': len(image_files)}
    
    if show_progress:
        print("✓ Pipeline initialized")
        print("\nProcessing pages...")
        print("="*70)
    
    # Track statistics
    stats = {
        'success': 0,
        'failed': 0,
        'total': len(image_files),
        'processing_times': [],
        'failed_files': []
    }
    
    # Process each image
    for idx, image_file in enumerate(image_files, 1):
        start_time = time.time()
        
        try:
            if show_progress:
                print(f"\n[{idx}/{len(image_files)}] Processing: {image_file.name}")
            
            # Run PP-StructureV3
            output = pipeline.predict(input=str(image_file))
            
            # Extract markdown from results
            markdown_list = []
            markdown_images_list = []
            
            for res in output:
                md_info = res.markdown
                markdown_list.append(md_info)
                markdown_images_list.append(md_info.get("markdown_images", {}))
            
            # If multiple pages (shouldn't happen for single images, but handle it)
            if len(markdown_list) > 1:
                markdown_text = pipeline.concatenate_markdown_pages(markdown_list)
            else:
                markdown_text = markdown_list[0]["markdown_texts"] if markdown_list else ""
            
            # Generate output filename (preserve page number from input)
            # e.g., page_003.png -> page_003.md
            output_filename = image_file.stem + ".md"
            output_file = output_path / output_filename
            
            # Save markdown file
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown_text)
            
            # Save any extracted images
            for item in markdown_images_list:
                if item:
                    for img_path, image in item.items():
                        # Save relative to output directory
                        img_file_path = output_path / img_path
                        img_file_path.parent.mkdir(parents=True, exist_ok=True)
                        image.save(str(img_file_path))
            
            elapsed = time.time() - start_time
            stats['processing_times'].append(elapsed)
            stats['success'] += 1
            
            if show_progress:
                print(f"  ✓ Saved: {output_filename} ({elapsed:.2f}s)")
            
        except Exception as e:
            elapsed = time.time() - start_time
            stats['failed'] += 1
            stats['failed_files'].append(image_file.name)
            
            if show_progress:
                print(f"  ✗ Failed: {image_file.name}")
                print(f"    Error: {str(e)[:100]}")
    
    return stats


def print_summary(stats, output_dir):
    """Print conversion summary"""
    print("\n" + "="*70)
    print("CONVERSION SUMMARY")
    print("="*70)
    print(f"Total files:      {stats['total']}")
    print(f"Successful:       {stats['success']}")
    print(f"Failed:           {stats['failed']}")
    try :
        if stats['processing_times']:
            avg_time = sum(stats['processing_times']) / len(stats['processing_times'])
            total_time = sum(stats['processing_times'])
            print(f"\nProcessing time:")
            print(f"  Average:        {avg_time:.2f}s per page")
            print(f"  Total:          {total_time:.2f}s")
        
        if stats['failed_files']:
            print(f"\nFailed files:")
            for filename in stats['failed_files']:
                print(f"  - {filename}")
        
        print(f"\nOutput directory: {output_dir}")
        print("="*70)
        
        if stats['success'] > 0:
            print(f"\n✓ Successfully converted {stats['success']} pages to Markdown!")
        
        if stats['failed'] > 0:
            print(f"\n⚠ {stats['failed']} pages failed to convert")
    except Exception as e:
        print(f"Error printing summary: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert document page images to Markdown files using PP-StructureV3',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all pages in a directory
  python convert_pages_to_markdown.py test_documents/nanonets_comparison
  
  # Specify custom output directory
  python convert_pages_to_markdown.py test_documents/nanonets_comparison -o output/my_markdown
  
  # Quiet mode (minimal output)
  python convert_pages_to_markdown.py test_documents/nanonets_comparison --quiet

Supported image formats:
  PNG, JPG, JPEG, BMP, TIFF
  
Output:
  - Markdown files named after input files (page_001.md, page_002.md, etc.)
  - Extracted images saved in subdirectories within output folder
        """
    )
    
    parser.add_argument('input_dir',
                        help='Directory containing page images to convert')
    parser.add_argument('--output', '-o', 
                        default='output/markdown_pages',
                        help='Output directory for markdown files (default: output/markdown_pages)')
    parser.add_argument('--quiet', '-q',
                        action='store_true',
                        help='Suppress progress messages')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("Page to Markdown Converter")
    print("Using PP-StructureV3 for document parsing")
    print("="*70)
    print(f"Input directory:  {args.input_dir}")
    print(f"Output directory: {args.output}")
    print()
    
    # Convert pages
    stats = convert_pages_to_markdown(
        args.input_dir,
        args.output,
        show_progress=not args.quiet
    )
    
    # Print summary
    if not args.quiet:
        print_summary(stats, args.output)
    else:
        print(f"Converted {stats['success']}/{stats['total']} pages successfully")


if __name__ == "__main__":
    main()

