"""
Download Test Documents for PaddleOCR Testing
Downloads various document types: research papers, forms, tables, invoices, etc.
"""

import os
import urllib.request
import ssl

def download_file(url, filepath, description):
    """Download a file with progress indication"""
    try:
        # Create SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        if os.path.exists(filepath):
            print(f"✓ {description} already exists")
            return True
        
        print(f"Downloading {description}...")
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, filepath)
        print(f"✓ Downloaded: {description}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {description}: {e}")
        return False

def main():
    """Download test documents"""
    print("="*60)
    print("Downloading Test Documents for PaddleOCR")
    print("="*60)
    
    # Create directories
    os.makedirs("test_documents", exist_ok=True)
    os.makedirs("test_documents/tables", exist_ok=True)
    os.makedirs("test_documents/forms", exist_ok=True)
    os.makedirs("test_documents/papers", exist_ok=True)
    os.makedirs("test_documents/invoices", exist_ok=True)
    os.makedirs("test_documents/mixed", exist_ok=True)
    
    test_documents = {
        # Tables
        "test_documents/tables/table_sample_1.jpg": {
            "url": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/ppstructure/docs/table/table.jpg",
            "description": "Table Sample 1 (financial data)"
        },
        "test_documents/tables/table_sample_2.jpg": {
            "url": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/doc/table/table.jpg",
            "description": "Table Sample 2 (structured table)"
        },
        
        # Forms and Documents
        "test_documents/forms/form_sample_1.jpg": {
            "url": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/ppstructure/docs/kie/input/zh_val_42.jpg",
            "description": "Form Sample 1 (Chinese form)"
        },
        "test_documents/forms/form_sample_2.jpg": {
            "url": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/doc/kie/input/zh_val_21.jpg",
            "description": "Form Sample 2 (document form)"
        },
        
        # Complex layouts
        "test_documents/papers/layout_sample_1.jpg": {
            "url": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/ppstructure/docs/layout/layout.jpg",
            "description": "Layout Sample 1 (multi-column paper)"
        },
        "test_documents/papers/layout_sample_2.jpg": {
            "url": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/doc/ppocr_v3/layout_publaynet.png",
            "description": "Layout Sample 2 (research paper layout)"
        },
        
        # Invoices
        "test_documents/invoices/invoice_1.jpg": {
            "url": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/doc/vqa/input/zh_val_0.jpg",
            "description": "Invoice Sample 1"
        },
        "test_documents/invoices/invoice_2.jpg": {
            "url": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/doc/vqa/input/zh_val_21.jpg",
            "description": "Invoice Sample 2"
        },
        
        # Mixed content (text + images + tables)
        "test_documents/mixed/paper_with_table.jpg": {
            "url": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/ppstructure/docs/recovery/result_normal/recovery.jpg",
            "description": "Mixed Content Sample (paper with tables)"
        },
        "test_documents/mixed/newspaper.jpg": {
            "url": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/doc/newspaper/newspaper_demo.jpg",
            "description": "Newspaper Layout Sample"
        },
        
        # Additional test images
        "test_documents/mixed/complex_layout.jpg": {
            "url": "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/release/2.7/doc/imgs_en/img_12.jpg",
            "description": "Complex Layout Document"
        },
    }
    
    print("\nDownloading test documents...")
    print("-" * 60)
    
    success_count = 0
    total_count = len(test_documents)
    
    for filepath, info in test_documents.items():
        if download_file(info["url"], filepath, info["description"]):
            success_count += 1
    
    print("\n" + "="*60)
    print(f"Download Summary: {success_count}/{total_count} files ready")
    print("="*60)
    
    print("\nTest documents organized by type:")
    print(f"  📊 Tables: test_documents/tables/")
    print(f"  📝 Forms: test_documents/forms/")
    print(f"  📄 Papers: test_documents/papers/")
    print(f"  🧾 Invoices: test_documents/invoices/")
    print(f"  🎨 Mixed: test_documents/mixed/")
    
    print("\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    print("\n1. Test Document Parsing:")
    print("   python test_document_parsing.py test_documents/papers/layout_sample_1.jpg")
    print("\n2. Test Table Recognition:")
    print("   python test_document_parsing.py test_documents/tables/table_sample_1.jpg --table")
    print("\n3. Test with Forms:")
    print("   python test_document_parsing.py test_documents/forms/form_sample_1.jpg")
    print("\n4. Test Multiple Documents:")
    print("   for file in test_documents/tables/*.jpg; do")
    print("       python test_document_parsing.py \"$file\" --table")
    print("   done")
    
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

