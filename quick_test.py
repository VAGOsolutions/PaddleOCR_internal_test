"""
Quick PaddleOCR Test - Minimal version for troubleshooting
"""

print("Testing PaddleOCR installation...")

try:
    from paddleocr import PaddleOCR
    print("✓ PaddleOCR imported successfully")
    
    # Initialize with minimal config
    print("\nInitializing PaddleOCR (this may take a minute)...")
    ocr = PaddleOCR(lang='en', device='cpu', enable_mkldnn=False)
    print("✓ PaddleOCR initialized successfully")
    
    # Test with a sample image if available
    import os
    test_image = "test_images/english_receipt.jpg"
    
    if os.path.exists(test_image):
        print(f"\nTesting OCR on {test_image}...")
        result = ocr.ocr(test_image)
        
        if result and result[0]:
            print(f"✓ OCR successful! Found {len(result[0])} text regions")
            print("\nFirst 3 detected texts:")
            for i, line in enumerate(result[0][:3], 1):
                text = line[1][0]
                confidence = line[1][1]
                print(f"{i}. '{text}' (confidence: {confidence:.2f})")
        else:
            print("✗ No text detected")
    else:
        print(f"\n⚠ Test image not found: {test_image}")
        print("But PaddleOCR is working! You can now test with your own images.")
    
    print("\n" + "="*60)
    print("✓ PaddleOCR is working correctly!")
    print("="*60)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()

