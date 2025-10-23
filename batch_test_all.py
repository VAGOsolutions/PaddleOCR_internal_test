"""
Batch OCR Testing - Process All Test Documents
Generates comprehensive results for model comparison
"""

import os
import glob
import json
import time
from datetime import datetime
from pathlib import Path

def batch_process_documents():
    """Process all test documents and generate comparison report"""
    
    print("="*70)
    print("PaddleOCR Batch Testing - Complete Document Set")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Import test function
    from test_basic_ocr import test_basic_ocr
    
    # Find all test documents
    test_patterns = [
        "test_documents/tables/*.jpg",
        "test_documents/invoices/*.jpg",
        "test_documents/forms/*.jpg",
        "test_documents/papers/*.jpg",
        "test_documents/mixed/*.jpg"
    ]
    
    all_documents = []
    for pattern in test_patterns:
        all_documents.extend(glob.glob(pattern))
    
    print(f"\nFound {len(all_documents)} test documents")
    print("-"*70)
    
    # Process each document
    results_summary = {
        "test_date": datetime.now().isoformat(),
        "total_documents": len(all_documents),
        "successful": 0,
        "failed": 0,
        "documents": []
    }
    
    for idx, doc_path in enumerate(all_documents, 1):
        doc_name = os.path.basename(doc_path)
        category = os.path.basename(os.path.dirname(doc_path))
        
        print(f"\n[{idx}/{len(all_documents)}] Processing: {category}/{doc_name}")
        print("-"*70)
        
        start_time = time.time()
        
        try:
            success = test_basic_ocr(doc_path, output_dir="test_results")
            processing_time = time.time() - start_time
            
            if success:
                # Load results to get text count
                json_path = os.path.join("test_results", 
                                        os.path.splitext(doc_name)[0] + ".json")
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Calculate average confidence
                confidences = [r['confidence'] for r in data['results']]
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                
                doc_result = {
                    "filename": doc_name,
                    "category": category,
                    "status": "success",
                    "text_regions": len(data['results']),
                    "avg_confidence": round(avg_confidence, 4),
                    "processing_time": round(processing_time, 2),
                    "output_files": {
                        "json": json_path,
                        "txt": json_path.replace('.json', '.txt'),
                        "image": json_path.replace('.json', '_annotated.jpg')
                    }
                }
                
                results_summary["successful"] += 1
                print(f"✓ Success: {len(data['results'])} regions, "
                      f"Avg confidence: {avg_confidence:.2%}, "
                      f"Time: {processing_time:.2f}s")
            else:
                doc_result = {
                    "filename": doc_name,
                    "category": category,
                    "status": "failed",
                    "processing_time": round(processing_time, 2)
                }
                results_summary["failed"] += 1
                print(f"✗ Failed")
                
        except Exception as e:
            processing_time = time.time() - start_time
            doc_result = {
                "filename": doc_name,
                "category": category,
                "status": "error",
                "error": str(e),
                "processing_time": round(processing_time, 2)
            }
            results_summary["failed"] += 1
            print(f"✗ Error: {e}")
        
        results_summary["documents"].append(doc_result)
    
    # Calculate statistics
    total_time = sum(d['processing_time'] for d in results_summary['documents'])
    results_summary["total_processing_time"] = round(total_time, 2)
    results_summary["avg_processing_time"] = round(total_time / len(all_documents), 2)
    
    # Save summary report
    summary_file = "test_results/BATCH_SUMMARY_REPORT.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(results_summary, f, indent=2, ensure_ascii=False)
    
    # Generate text report
    generate_text_report(results_summary)
    
    # Generate comparison table
    generate_comparison_table(results_summary)
    
    print("\n" + "="*70)
    print("Batch Processing Complete!")
    print("="*70)
    print(f"\nSummary:")
    print(f"  Total documents: {results_summary['total_documents']}")
    print(f"  Successful: {results_summary['successful']}")
    print(f"  Failed: {results_summary['failed']}")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Average time: {results_summary['avg_processing_time']:.2f}s per document")
    print(f"\nReports saved:")
    print(f"  - test_results/BATCH_SUMMARY_REPORT.json")
    print(f"  - test_results/BATCH_SUMMARY_REPORT.txt")
    print(f"  - test_results/COMPARISON_TABLE.md")
    
    return results_summary

def generate_text_report(results_summary):
    """Generate human-readable text report"""
    
    report_file = "test_results/BATCH_SUMMARY_REPORT.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("PaddleOCR Batch Testing - Complete Summary Report\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Test Date: {results_summary['test_date']}\n")
        f.write(f"Total Documents: {results_summary['total_documents']}\n")
        f.write(f"Successful: {results_summary['successful']}\n")
        f.write(f"Failed: {results_summary['failed']}\n")
        f.write(f"Success Rate: {results_summary['successful']/results_summary['total_documents']*100:.1f}%\n")
        f.write(f"Total Processing Time: {results_summary['total_processing_time']:.2f}s\n")
        f.write(f"Average Processing Time: {results_summary['avg_processing_time']:.2f}s\n\n")
        
        # Group by category
        categories = {}
        for doc in results_summary['documents']:
            cat = doc['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(doc)
        
        for category, docs in sorted(categories.items()):
            f.write("="*70 + "\n")
            f.write(f"Category: {category.upper()}\n")
            f.write("="*70 + "\n\n")
            
            for doc in docs:
                f.write(f"Document: {doc['filename']}\n")
                f.write(f"  Status: {doc['status']}\n")
                
                if doc['status'] == 'success':
                    f.write(f"  Text Regions: {doc['text_regions']}\n")
                    f.write(f"  Avg Confidence: {doc['avg_confidence']:.4f} ({doc['avg_confidence']*100:.2f}%)\n")
                    f.write(f"  Processing Time: {doc['processing_time']:.2f}s\n")
                elif doc['status'] == 'error':
                    f.write(f"  Error: {doc.get('error', 'Unknown')}\n")
                
                f.write("\n")
    
    print(f"✓ Text report saved to: {report_file}")

def generate_comparison_table(results_summary):
    """Generate markdown comparison table"""
    
    table_file = "test_results/COMPARISON_TABLE.md"
    
    with open(table_file, 'w', encoding='utf-8') as f:
        f.write("# PaddleOCR Test Results - Model Comparison Ready\n\n")
        f.write(f"**Test Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**Model:** PaddleOCR v3.3.0 (PP-OCRv5)  \n")
        f.write(f"**Total Documents:** {results_summary['total_documents']}  \n\n")
        
        f.write("## Summary Statistics\n\n")
        f.write(f"- **Success Rate:** {results_summary['successful']}/{results_summary['total_documents']} ")
        f.write(f"({results_summary['successful']/results_summary['total_documents']*100:.1f}%)\n")
        f.write(f"- **Total Processing Time:** {results_summary['total_processing_time']:.2f}s\n")
        f.write(f"- **Average Time per Document:** {results_summary['avg_processing_time']:.2f}s\n\n")
        
        f.write("## Detailed Results by Document\n\n")
        f.write("| Category | Document | Text Regions | Avg Confidence | Time (s) | Status |\n")
        f.write("|----------|----------|--------------|----------------|----------|--------|\n")
        
        for doc in results_summary['documents']:
            if doc['status'] == 'success':
                f.write(f"| {doc['category']} | {doc['filename']} | "
                       f"{doc['text_regions']} | {doc['avg_confidence']:.4f} | "
                       f"{doc['processing_time']:.2f} | ✅ |\n")
            else:
                f.write(f"| {doc['category']} | {doc['filename']} | "
                       f"- | - | {doc['processing_time']:.2f} | ❌ |\n")
        
        f.write("\n## Results by Category\n\n")
        
        # Group statistics by category
        categories = {}
        for doc in results_summary['documents']:
            cat = doc['category']
            if cat not in categories:
                categories[cat] = {'count': 0, 'success': 0, 'total_regions': 0, 
                                  'total_confidence': 0, 'total_time': 0}
            
            categories[cat]['count'] += 1
            if doc['status'] == 'success':
                categories[cat]['success'] += 1
                categories[cat]['total_regions'] += doc['text_regions']
                categories[cat]['total_confidence'] += doc['avg_confidence']
            categories[cat]['total_time'] += doc['processing_time']
        
        f.write("| Category | Documents | Success Rate | Avg Regions | Avg Confidence | Avg Time (s) |\n")
        f.write("|----------|-----------|--------------|-------------|----------------|-------------|\n")
        
        for cat, stats in sorted(categories.items()):
            success_rate = stats['success'] / stats['count'] * 100
            avg_regions = stats['total_regions'] / stats['success'] if stats['success'] > 0 else 0
            avg_conf = stats['total_confidence'] / stats['success'] if stats['success'] > 0 else 0
            avg_time = stats['total_time'] / stats['count']
            
            f.write(f"| {cat} | {stats['count']} | {success_rate:.0f}% | "
                   f"{avg_regions:.0f} | {avg_conf:.4f} | {avg_time:.2f} |\n")
        
        f.write("\n## Model Comparison Template\n\n")
        f.write("Use this table to compare with other OCR models:\n\n")
        f.write("| Model | Total Time (s) | Avg Time (s) | Avg Confidence | Success Rate | Notes |\n")
        f.write("|-------|----------------|--------------|----------------|--------------|-------|\n")
        f.write(f"| **PaddleOCR v3.3.0** | {results_summary['total_processing_time']:.2f} | ")
        f.write(f"{results_summary['avg_processing_time']:.2f} | ")
        
        # Calculate overall avg confidence
        total_conf = sum(d.get('avg_confidence', 0) for d in results_summary['documents'] if d['status'] == 'success')
        avg_conf = total_conf / results_summary['successful'] if results_summary['successful'] > 0 else 0
        f.write(f"{avg_conf:.4f} | {results_summary['successful']}/{results_summary['total_documents']} | Baseline |\n")
        f.write("| Tesseract | - | - | - | - | Add results |\n")
        f.write("| EasyOCR | - | - | - | - | Add results |\n")
        f.write("| Other Model | - | - | - | - | Add results |\n")
        
        f.write("\n---\n\n")
        f.write("**Ready for comparison testing with other OCR models.**\n")
    
    print(f"✓ Comparison table saved to: {table_file}")

if __name__ == "__main__":
    batch_process_documents()

