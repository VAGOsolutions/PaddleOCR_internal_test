"""
Basic OCR Testing Script for PaddleOCR
Tests text detection and recognition capabilities
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

def test_basic_ocr(image_path, output_dir="test_results"):
    """
    Test basic OCR functionality
    
    Args:
        image_path: Path to the test image
        output_dir: Directory to save results
    """
    try:
        from paddleocr import PaddleOCR
        import cv2
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont
        
        print("\n" + "="*60)
        print("Testing Basic OCR (PP-OCRv5)")
        print("="*60)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize PaddleOCR
        print("\nInitializing PaddleOCR...")
        ocr = PaddleOCR(
            use_textline_orientation=True,
            lang='en'
        )
        
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"✗ Image not found: {image_path}")
            print("Please provide a valid image path or use download_test_images() first")
            return False
        
        print(f"✓ Processing image: {image_path}")
        
        # Perform OCR
        result = ocr.predict(image_path)
        
        # Process results
        if result and result[0]:
            ocr_result = result[0]
            
            # Extract texts and scores from OCRResult object
            texts = ocr_result.get('rec_texts', [])
            scores = ocr_result.get('rec_scores', [])
            boxes = ocr_result.get('rec_polys', [])
            
            print(f"✓ Found {len(texts)} text regions\n")
            
            # Save results to JSON
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "image_path": str(image_path),
                "total_regions": len(texts),
                "results": []
            }
            
            print("Detected Text:")
            print("-" * 60)
            for idx, (text, score) in enumerate(zip(texts, scores), 1):
                box = boxes[idx-1] if idx-1 < len(boxes) else []
                
                print(f"{idx}. Text: '{text}'")
                print(f"   Confidence: {score:.4f}")
                if hasattr(box, 'tolist'):
                    box_list = box.tolist()
                else:
                    box_list = box
                print(f"   Box: {box_list[:4] if len(str(box_list)) > 100 else box_list}\n")
                
                output_data["results"].append({
                    "index": idx,
                    "text": text,
                    "confidence": float(score),
                    "box": box_list if hasattr(box, 'tolist') else (list(box) if isinstance(box, (list, tuple)) else str(box))
                })
            
            # Save results in multiple formats
            input_basename = os.path.basename(image_path)
            name_without_ext = os.path.splitext(input_basename)[0]
            
            print("\n" + "="*60)
            print("Saving Results")
            print("="*60)
            
            # 1. Save JSON file (structured data with coordinates and confidence)
            json_file = os.path.join(output_dir, f"{name_without_ext}.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"✓ JSON saved to: {json_file}")
            
            # 2. Save plain text file (extracted text only)
            txt_file = os.path.join(output_dir, f"{name_without_ext}.txt")
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"OCR Results for: {image_path}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Total text regions: {len(texts)}\n")
                f.write("="*60 + "\n\n")
                
                # Write all extracted text
                for idx, (text, score) in enumerate(zip(texts, scores), 1):
                    f.write(f"{idx}. {text}\n")
                
                f.write("\n" + "="*60 + "\n")
                f.write("Detailed Results with Confidence Scores:\n")
                f.write("="*60 + "\n\n")
                
                for idx, (text, score) in enumerate(zip(texts, scores), 1):
                    f.write(f"{idx:3d}. {text:50s} (confidence: {score:.4f})\n")
            print(f"✓ Text saved to: {txt_file}")
            
            # 3. Save visualization image (with bounding boxes)
            try:
                viz_file = os.path.join(output_dir, f"{name_without_ext}_annotated.jpg")
                ocr_result.save_to_img(viz_file)
                print(f"✓ Visualization saved to: {viz_file}")
            except Exception as e:
                print(f"⚠ Could not create visualization: {e}")
            
            return True
        else:
            print("✗ No text detected in the image")
            return False
            
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please install required packages: pip install paddleocr[all]")
        return False
    except Exception as e:
        print(f"✗ Error during OCR: {e}")
        import traceback
        traceback.print_exc()
        return False


def download_test_images(output_dir="test_images"):
    """
    Download sample test images for OCR testing
    
    Args:
        output_dir: Directory to save test images
    """
    try:
        import urllib.request
        import ssl
        
        print("\n" + "="*60)
        print("Downloading Test Images")
        print("="*60)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Create SSL context to handle certificate verification
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        test_images = {
            "english_receipt.jpg": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/doc/imgs_en/254.jpg",
            "chinese_document.jpg": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/doc/imgs/11.jpg",
            "mixed_text.jpg": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/doc/imgs_en/img_12.jpg"
        }
        
        downloaded_files = []
        for filename, url in test_images.items():
            filepath = os.path.join(output_dir, filename)
            if os.path.exists(filepath):
                print(f"✓ {filename} already exists")
                downloaded_files.append(filepath)
            else:
                try:
                    print(f"Downloading {filename}...")
                    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(url, filepath)
                    print(f"✓ Downloaded: {filename}")
                    downloaded_files.append(filepath)
                except Exception as e:
                    print(f"✗ Failed to download {filename}: {e}")
        
        print(f"\n✓ Total images available: {len(downloaded_files)}")
        return downloaded_files
        
    except Exception as e:
        print(f"✗ Error downloading images: {e}")
        return []


def main():
    """Main testing function"""
    print("="*60)
    print("PaddleOCR Basic Testing Suite")
    print("="*60)
    
    # Download test images
    test_images = download_test_images()
    
    if not test_images:
        print("\n⚠ No test images available. Please provide your own images.")
        print("Usage: python test_basic_ocr.py <path_to_your_image>")
        return
    
    # Test with first available image
    print(f"\nTesting with: {test_images[0]}")
    success = test_basic_ocr(test_images[0])
    
    if success:
        print("\n" + "="*60)
        print("✓ Basic OCR Test Completed Successfully!")
        print("="*60)
        print("\nNext steps:")
        print("1. Check the test_results/ folder for outputs")
        print("2. Try other test scripts: test_document_parsing.py, test_table_recognition.py")
        print("3. Test with your own images")
    else:
        print("\n" + "="*60)
        print("✗ Basic OCR Test Failed")
        print("="*60)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Use provided image path
        image_path = sys.argv[1]
        test_basic_ocr(image_path)
    else:
        # Run full test suite
        main()

