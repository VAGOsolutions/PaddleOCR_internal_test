"""
Document Parsing Testing Script for PaddleOCR
Tests PP-StructureV3 capabilities including layout analysis, table recognition, etc.
"""

import os
import sys
import json
from datetime import datetime

def test_document_parsing(image_path, output_dir="test_results/document_parsing"):
    """
    Test document parsing functionality (PP-StructureV3)
    
    Args:
        image_path: Path to the test document image/PDF
        output_dir: Directory to save results
    """
    try:
        from paddleocr import PPStructure
        from PIL import Image
        
        print("\n" + "="*60)
        print("Testing Document Parsing (PP-StructureV3)")
        print("="*60)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize PP-Structure
        print("\nInitializing PP-StructureV3...")
        print("This may take a few moments on first run (downloading models)...")
        
        structure = PPStructure(
            show_log=False,
            use_gpu=False,
            lang='en'
        )
        
        # Check if document exists
        if not os.path.exists(image_path):
            print(f"✗ Document not found: {image_path}")
            return False
        
        print(f"✓ Processing document: {image_path}")
        
        # Perform document parsing
        result = structure(image_path)
        
        # Process results
        if result:
            print(f"✓ Found {len(result)} layout elements\n")
            
            # Save results
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "document_path": str(image_path),
                "total_elements": len(result),
                "elements": []
            }
            
            print("Layout Analysis:")
            print("-" * 60)
            
            element_counts = {}
            for idx, element in enumerate(result, 1):
                element_type = element.get('type', 'unknown')
                bbox = element.get('bbox', [])
                
                element_counts[element_type] = element_counts.get(element_type, 0) + 1
                
                print(f"{idx}. Type: {element_type}")
                print(f"   BBox: {bbox}")
                
                element_data = {
                    "index": idx,
                    "type": element_type,
                    "bbox": bbox
                }
                
                # Add text content if available
                if 'res' in element:
                    if element_type == 'table':
                        print(f"   Table HTML saved")
                        element_data['html'] = element['res'].get('html', '')
                    else:
                        text_lines = element['res']
                        if text_lines:
                            print(f"   Text lines: {len(text_lines)}")
                            element_data['text_lines'] = [
                                {"text": line['text'], "confidence": line.get('confidence', 0)}
                                for line in text_lines if isinstance(line, dict)
                            ]
                
                print()
                output_data["elements"].append(element_data)
            
            # Print summary
            print("Summary:")
            print("-" * 60)
            for elem_type, count in element_counts.items():
                print(f"  {elem_type}: {count}")
            
            # Save results
            result_file = os.path.join(output_dir, "document_parsing_results.json")
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Results saved to: {result_file}")
            
            return True
        else:
            print("✗ No elements detected in the document")
            return False
            
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please install required packages: pip install paddleocr[all]")
        return False
    except Exception as e:
        print(f"✗ Error during document parsing: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_table_recognition(image_path, output_dir="test_results/table_recognition"):
    """
    Test table recognition specifically
    
    Args:
        image_path: Path to the table image
        output_dir: Directory to save results
    """
    try:
        from paddleocr import PPStructure
        import pandas as pd
        from bs4 import BeautifulSoup
        
        print("\n" + "="*60)
        print("Testing Table Recognition")
        print("="*60)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize with table recognition
        print("\nInitializing Table Recognition...")
        structure = PPStructure(
            table=True,
            show_log=False,
            use_gpu=False
        )
        
        if not os.path.exists(image_path):
            print(f"✗ Image not found: {image_path}")
            return False
        
        print(f"✓ Processing table image: {image_path}")
        
        # Perform table recognition
        result = structure(image_path)
        
        # Process results
        tables_found = 0
        for idx, element in enumerate(result, 1):
            if element.get('type') == 'table':
                tables_found += 1
                print(f"\n✓ Found table #{tables_found}")
                
                if 'res' in element and 'html' in element['res']:
                    html = element['res']['html']
                    
                    # Save HTML
                    html_file = os.path.join(output_dir, f"table_{tables_found}.html")
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(html)
                    print(f"  HTML saved to: {html_file}")
                    
                    # Try to convert to CSV
                    try:
                        soup = BeautifulSoup(html, 'html.parser')
                        table = soup.find('table')
                        if table:
                            rows = []
                            for tr in table.find_all('tr'):
                                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                                rows.append(cells)
                            
                            if rows:
                                df = pd.DataFrame(rows[1:], columns=rows[0] if rows else None)
                                csv_file = os.path.join(output_dir, f"table_{tables_found}.csv")
                                df.to_csv(csv_file, index=False, encoding='utf-8')
                                print(f"  CSV saved to: {csv_file}")
                                print(f"  Rows: {len(df)}, Columns: {len(df.columns)}")
                    except Exception as e:
                        print(f"  ⚠ Could not convert to CSV: {e}")
        
        if tables_found > 0:
            print(f"\n✓ Total tables found: {tables_found}")
            return True
        else:
            print("\n✗ No tables detected in the image")
            return False
            
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please install: pip install paddleocr[all] beautifulsoup4")
        return False
    except Exception as e:
        print(f"✗ Error during table recognition: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main testing function"""
    print("="*60)
    print("PaddleOCR Document Parsing Test Suite")
    print("="*60)
    
    if len(sys.argv) > 1:
        doc_path = sys.argv[1]
        print(f"\nTesting with provided document: {doc_path}")
        
        # Test document parsing
        test_document_parsing(doc_path)
        
        # Ask if it's a table
        print("\n" + "="*60)
        print("For table-specific testing, use: python test_document_parsing.py <image> --table")
    else:
        print("\nUsage:")
        print("  python test_document_parsing.py <path_to_document>")
        print("  python test_document_parsing.py <path_to_table_image> --table")
        print("\nExample documents to test with:")
        print("  - Invoices and receipts")
        print("  - Research papers with tables")
        print("  - Forms and certificates")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if '--table' in sys.argv:
            image_path = sys.argv[1]
            test_table_recognition(image_path)
        else:
            image_path = sys.argv[1]
            test_document_parsing(image_path)
    else:
        main()

