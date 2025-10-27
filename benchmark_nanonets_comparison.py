"""
Benchmark Script for Nanonets vs PaddleOCR Comparison
Tracks detailed performance metrics including time, memory, accuracy
"""

import os
import sys
import glob
import json
import time
import csv
from datetime import datetime
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
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not available. Memory tracking will be limited.")


class PerformanceTracker:
    """Track performance metrics for OCR operations"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.start_memory = None
        self.peak_memory = None
        self.process = psutil.Process() if PSUTIL_AVAILABLE else None
    
    def start(self):
        """Start tracking"""
        self.start_time = time.perf_counter()
        if self.process:
            self.start_memory = self.process.memory_info().rss / (1024 * 1024)  # MB
            self.peak_memory = self.start_memory
    
    def update_peak_memory(self):
        """Update peak memory usage"""
        if self.process:
            current_memory = self.process.memory_info().rss / (1024 * 1024)  # MB
            self.peak_memory = max(self.peak_memory, current_memory)
    
    def stop(self):
        """Stop tracking and return metrics"""
        self.end_time = time.perf_counter()
        self.update_peak_memory()
        
        elapsed_time = self.end_time - self.start_time
        
        metrics = {
            "elapsed_time_seconds": round(elapsed_time, 4),
            "elapsed_time_ms": round(elapsed_time * 1000, 2)
        }
        
        if self.process:
            end_memory = self.process.memory_info().rss / (1024 * 1024)  # MB
            metrics.update({
                "start_memory_mb": round(self.start_memory, 2),
                "end_memory_mb": round(end_memory, 2),
                "peak_memory_mb": round(self.peak_memory, 2),
                "memory_increase_mb": round(end_memory - self.start_memory, 2)
            })
        
        return metrics


def perform_ocr_with_metrics(image_path, ocr_engine):
    """
    Perform OCR on an image and track detailed metrics
    
    Args:
        image_path: Path to image file
        ocr_engine: Initialized PaddleOCR instance
        
    Returns:
        Dictionary with OCR results and performance metrics
    """
    tracker = PerformanceTracker()
    
    print(f"\nProcessing: {os.path.basename(image_path)}")
    print("-" * 70)
    
    tracker.start()
    
    try:
        # Perform OCR
        result = ocr_engine.predict(image_path)
        
        # Update memory during processing
        tracker.update_peak_memory()
        
        # Stop tracking
        performance_metrics = tracker.stop()
        
        # Process results
        if result and result[0]:
            ocr_result = result[0]
            
            # Extract texts and scores
            texts = ocr_result.get('rec_texts', [])
            scores = ocr_result.get('rec_scores', [])
            boxes = ocr_result.get('rec_polys', [])
            
            # Calculate metrics
            total_chars = sum(len(text) for text in texts)
            avg_confidence = sum(scores) / len(scores) if scores else 0
            min_confidence = min(scores) if scores else 0
            max_confidence = max(scores) if scores else 0
            
            # Count high/medium/low confidence predictions
            high_conf = sum(1 for s in scores if s >= 0.9)
            medium_conf = sum(1 for s in scores if 0.7 <= s < 0.9)
            low_conf = sum(1 for s in scores if s < 0.7)
            
            ocr_metrics = {
                "success": True,
                "text_regions": len(texts),
                "total_characters": total_chars,
                "confidence_scores": {
                    "average": round(avg_confidence, 4),
                    "min": round(min_confidence, 4),
                    "max": round(max_confidence, 4)
                },
                "confidence_distribution": {
                    "high (≥0.9)": high_conf,
                    "medium (0.7-0.9)": medium_conf,
                    "low (<0.7)": low_conf
                },
                "extracted_texts": texts,
                "confidence_list": [round(s, 4) for s in scores],
                "bounding_boxes": [box.tolist() if hasattr(box, 'tolist') else list(box) for box in boxes]
            }
            
            print(f"✓ Text regions detected: {len(texts)}")
            print(f"✓ Total characters: {total_chars}")
            print(f"✓ Average confidence: {avg_confidence:.2%}")
            print(f"✓ Processing time: {performance_metrics['elapsed_time_ms']:.2f} ms")
            if PSUTIL_AVAILABLE:
                print(f"✓ Peak memory: {performance_metrics['peak_memory_mb']:.2f} MB")
            
            return {
                "ocr_result": ocr_result,
                "metrics": ocr_metrics,
                "performance": performance_metrics
            }
        else:
            performance_metrics = tracker.stop()
            print("✗ No text detected")
            
            return {
                "ocr_result": None,
                "metrics": {
                    "success": False,
                    "text_regions": 0,
                    "error": "No text detected"
                },
                "performance": performance_metrics
            }
            
    except Exception as e:
        performance_metrics = tracker.stop()
        print(f"✗ Error: {e}")
        
        return {
            "ocr_result": None,
            "metrics": {
                "success": False,
                "error": str(e)
            },
            "performance": performance_metrics
        }


def save_results(image_path, result_data, output_dir):
    """
    Save OCR results in multiple formats
    
    Args:
        image_path: Path to source image
        result_data: Dictionary with OCR results and metrics
        output_dir: Directory to save results
    """
    os.makedirs(output_dir, exist_ok=True)
    
    basename = os.path.basename(image_path)
    name_without_ext = os.path.splitext(basename)[0]
    
    # 1. Save comprehensive JSON with all metrics
    json_file = os.path.join(output_dir, f"{name_without_ext}.json")
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "source_image": str(image_path),
        "image_name": basename,
        "ocr_metrics": result_data["metrics"],
        "performance_metrics": result_data["performance"]
    }
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"  → Saved JSON: {json_file}")
    
    # 2. Save plain text extraction
    if result_data["metrics"].get("success"):
        txt_file = os.path.join(output_dir, f"{name_without_ext}.txt")
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"OCR Results for: {basename}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write("="*70 + "\n\n")
            
            texts = result_data["metrics"]["extracted_texts"]
            confidences = result_data["metrics"]["confidence_list"]
            
            f.write("EXTRACTED TEXT:\n")
            f.write("-"*70 + "\n")
            for text in texts:
                f.write(f"{text}\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("DETAILED RESULTS WITH CONFIDENCE:\n")
            f.write("="*70 + "\n\n")
            
            for idx, (text, conf) in enumerate(zip(texts, confidences), 1):
                f.write(f"{idx:3d}. [{conf:.4f}] {text}\n")
        
        print(f"  → Saved TXT: {txt_file}")
        
        # 3. Save annotated visualization
        try:
            viz_file = os.path.join(output_dir, f"{name_without_ext}_annotated.jpg")
            result_data["ocr_result"].save_to_img(viz_file)
            print(f"  → Saved Visualization: {viz_file}")
        except Exception as e:
            print(f"  ⚠ Could not save visualization: {e}")


def benchmark_all_pages(input_dir="test_documents/nanonets_comparison", 
                        output_dir="test_results/nanonets_comparison"):
    """
    Run benchmark on all extracted pages
    
    Args:
        input_dir: Directory with extracted page images
        output_dir: Directory to save results
    """
    print("\n" + "="*70)
    print("PaddleOCR Benchmark - Nanonets Comparison")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Find all images
    image_patterns = [
        os.path.join(input_dir, "*.png"),
        os.path.join(input_dir, "*.jpg"),
        os.path.join(input_dir, "*.jpeg")
    ]
    
    all_images = []
    for pattern in image_patterns:
        all_images.extend(glob.glob(pattern))
    
    all_images = sorted(all_images)
    
    if not all_images:
        print(f"\n✗ No images found in {input_dir}")
        print("\nPlease run: python extract_pdf_pages.py --pages \"<page_numbers>\"")
        return None
    
    print(f"\nFound {len(all_images)} images to process")
    
    # Initialize PaddleOCR
    print("\nInitializing PaddleOCR (PP-OCRv5)...")
    try:
        from paddleocr import PaddleOCR
        
        init_start = time.time()
        ocr = PaddleOCR(
            use_textline_orientation=True,
            lang='en'
        )
        init_time = time.time() - init_start
        print(f"✓ PaddleOCR initialized in {init_time:.2f}s")
    except Exception as e:
        print(f"✗ Failed to initialize PaddleOCR: {e}")
        return None
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each image
    all_results = []
    total_tracker = PerformanceTracker()
    total_tracker.start()
    
    print("\n" + "="*70)
    print("Processing Images")
    print("="*70)
    
    for idx, image_path in enumerate(all_images, 1):
        print(f"\n[{idx}/{len(all_images)}] {os.path.basename(image_path)}")
        print("="*70)
        
        # Perform OCR with metrics
        result_data = perform_ocr_with_metrics(image_path, ocr)
        
        # Save results
        save_results(image_path, result_data, output_dir)
        
        # Store for summary
        all_results.append({
            "image_name": os.path.basename(image_path),
            "image_path": image_path,
            **result_data["metrics"],
            "performance": result_data["performance"]
        })
    
    total_metrics = total_tracker.stop()
    
    # Generate summary report
    summary = generate_summary_report(all_results, total_metrics, output_dir)
    
    # Generate comparison report
    generate_comparison_report(summary, output_dir)
    
    # Generate CSV export
    generate_csv_export(all_results, output_dir)
    
    print("\n" + "="*70)
    print("Benchmark Complete!")
    print("="*70)
    print(f"\nProcessed: {len(all_images)} images")
    print(f"Total time: {total_metrics['elapsed_time_seconds']:.2f}s")
    print(f"Average time per page: {total_metrics['elapsed_time_seconds']/len(all_images):.2f}s")
    print(f"\nResults saved to: {output_dir}")
    
    return summary


def generate_summary_report(all_results, total_metrics, output_dir):
    """Generate comprehensive summary report"""
    
    successful = [r for r in all_results if r.get("success")]
    failed = [r for r in all_results if not r.get("success")]
    
    # Calculate aggregate statistics
    total_text_regions = sum(r.get("text_regions", 0) for r in successful)
    total_characters = sum(r.get("total_characters", 0) for r in successful)
    
    if successful:
        avg_confidence = sum(r.get("confidence_scores", {}).get("average", 0) for r in successful) / len(successful)
        avg_regions_per_page = total_text_regions / len(successful)
        avg_chars_per_page = total_characters / len(successful)
    else:
        avg_confidence = 0
        avg_regions_per_page = 0
        avg_chars_per_page = 0
    
    summary = {
        "test_info": {
            "timestamp": datetime.now().isoformat(),
            "ocr_engine": "PaddleOCR v3.3.0 (PP-OCRv5) - (PaddleOCR-VL)",
            "total_images": len(all_results),
            "successful": len(successful),
            "failed": len(failed)
        },
        "aggregate_metrics": {
            "total_text_regions": total_text_regions,
            "total_characters": total_characters,
            "average_confidence": round(avg_confidence, 4),
            "average_regions_per_page": round(avg_regions_per_page, 2),
            "average_characters_per_page": round(avg_chars_per_page, 2)
        },
        "performance_metrics": {
            "total_processing_time_seconds": total_metrics["elapsed_time_seconds"],
            "average_time_per_page_seconds": round(total_metrics["elapsed_time_seconds"] / len(all_results), 4),
            "average_time_per_page_ms": round((total_metrics["elapsed_time_seconds"] / len(all_results)) * 1000, 2)
        },
        "detailed_results": all_results
    }
    
    if PSUTIL_AVAILABLE:
        summary["performance_metrics"].update({
            "peak_memory_mb": total_metrics.get("peak_memory_mb", 0),
            "memory_increase_mb": total_metrics.get("memory_increase_mb", 0)
        })
    
    # Save summary JSON
    summary_file = os.path.join(output_dir, "nanonets_comparison_results.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Summary report saved: {summary_file}")
    
    return summary


def generate_comparison_report(summary, output_dir):
    """Generate markdown comparison report for sharing with colleagues"""
    
    report_file = os.path.join(output_dir, "NANONETS_COMPARISON_REPORT.md")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# OCR Benchmark Results - PaddleOCR vs Nanonets\n\n")
        f.write(f"**Test Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**Document:** IBM Cloud Foundations Benchmark v1.1.0  \n")
        f.write(f"**Pages Tested:** {summary['test_info']['total_images']}  \n\n")
        
        f.write("---\n\n")
        f.write("## PaddleOCR Results\n\n")
        
        # Overview statistics
        f.write("### Overview\n\n")
        f.write(f"- **OCR Engine:** {summary['test_info']['ocr_engine']}\n")
        f.write(f"- **Total Pages:** {summary['test_info']['total_images']}\n")
        f.write(f"- **Successfully Processed:** {summary['test_info']['successful']}\n")
        f.write(f"- **Failed:** {summary['test_info']['failed']}\n")
        f.write(f"- **Success Rate:** {summary['test_info']['successful']/summary['test_info']['total_images']*100:.1f}%\n\n")
        
        # Accuracy metrics
        f.write("### Accuracy Metrics\n\n")
        agg = summary['aggregate_metrics']
        f.write(f"- **Total Text Regions Detected:** {agg['total_text_regions']}\n")
        f.write(f"- **Total Characters Extracted:** {agg['total_characters']}\n")
        f.write(f"- **Average Confidence Score:** {agg['average_confidence']:.4f} ({agg['average_confidence']*100:.2f}%)\n")
        f.write(f"- **Average Regions per Page:** {agg['average_regions_per_page']:.1f}\n")
        f.write(f"- **Average Characters per Page:** {agg['average_characters_per_page']:.1f}\n\n")
        
        # Performance metrics
        f.write("### Performance Metrics\n\n")
        perf = summary['performance_metrics']
        f.write(f"- **Total Processing Time:** {perf['total_processing_time_seconds']:.2f} seconds\n")
        f.write(f"- **Average Time per Page:** {perf['average_time_per_page_seconds']:.4f}s ({perf['average_time_per_page_ms']:.2f}ms)\n")
        
        if PSUTIL_AVAILABLE:
            f.write(f"- **Peak Memory Usage:** {perf.get('peak_memory_mb', 0):.2f} MB\n")
        
        f.write("\n### Per-Page Results\n\n")
        f.write("| Page | Text Regions | Characters | Avg Confidence | Time (ms) | Status |\n")
        f.write("|------|--------------|------------|----------------|-----------|--------|\n")
        
        for result in summary['detailed_results']:
            page_name = result['image_name']
            if result.get('success'):
                regions = result.get('text_regions', 0)
                chars = result.get('total_characters', 0)
                conf = result.get('confidence_scores', {}).get('average', 0)
                time_ms = result['performance']['elapsed_time_ms']
                status = "✅"
                f.write(f"| {page_name} | {regions} | {chars} | {conf:.4f} | {time_ms:.2f} | {status} |\n")
            else:
                time_ms = result['performance']['elapsed_time_ms']
                status = "❌"
                f.write(f"| {page_name} | - | - | - | {time_ms:.2f} | {status} |\n")
        
        # Comparison template
        f.write("\n---\n\n")
        f.write("## Side-by-Side Comparison\n\n")
        f.write("Use this table to add Nanonets results for comparison:\n\n")
        f.write("| Metric | PaddleOCR | Nanonets | Winner |\n")
        f.write("|--------|-----------|----------|--------|\n")
        f.write(f"| **Total Processing Time (s)** | {perf['total_processing_time_seconds']:.2f} | _[Add result]_ | |\n")
        f.write(f"| **Avg Time per Page (ms)** | {perf['average_time_per_page_ms']:.2f} | _[Add result]_ | |\n")
        f.write(f"| **Avg Confidence Score** | {agg['average_confidence']:.4f} | _[Add result]_ | |\n")
        f.write(f"| **Total Text Regions** | {agg['total_text_regions']} | _[Add result]_ | |\n")
        f.write(f"| **Total Characters** | {agg['total_characters']} | _[Add result]_ | |\n")
        f.write(f"| **Success Rate** | {summary['test_info']['successful']}/{summary['test_info']['total_images']} | _[Add result]_ | |\n")
        
        if PSUTIL_AVAILABLE:
            f.write(f"| **Peak Memory (MB)** | {perf.get('peak_memory_mb', 0):.2f} | _[Add result]_ | |\n")
        
        f.write("\n### Notes\n\n")
        f.write("- All times measured on the same hardware\n")
        f.write("- Pages selected for complexity (tables, dense text, technical content)\n")
        f.write("- Confidence scores range from 0.0 to 1.0\n")
        f.write("\n---\n\n")
        f.write("*Generated automatically by PaddleOCR benchmark script*\n")
    
    print(f"✓ Comparison report saved: {report_file}")


def generate_csv_export(all_results, output_dir):
    """Generate CSV export for easy spreadsheet analysis"""
    
    csv_file = os.path.join(output_dir, "performance_metrics.csv")
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        header = [
            "Page Name",
            "Success",
            "Text Regions",
            "Total Characters",
            "Avg Confidence",
            "Min Confidence",
            "Max Confidence",
            "High Conf (≥0.9)",
            "Medium Conf (0.7-0.9)",
            "Low Conf (<0.7)",
            "Processing Time (s)",
            "Processing Time (ms)"
        ]
        
        if PSUTIL_AVAILABLE:
            header.extend(["Peak Memory (MB)", "Memory Increase (MB)"])
        
        writer.writerow(header)
        
        # Data rows
        for result in all_results:
            row = [
                result['image_name'],
                "Yes" if result.get('success') else "No"
            ]
            
            if result.get('success'):
                conf_scores = result.get('confidence_scores', {})
                conf_dist = result.get('confidence_distribution', {})
                row.extend([
                    result.get('text_regions', 0),
                    result.get('total_characters', 0),
                    conf_scores.get('average', 0),
                    conf_scores.get('min', 0),
                    conf_scores.get('max', 0),
                    conf_dist.get('high (≥0.9)', 0),
                    conf_dist.get('medium (0.7-0.9)', 0),
                    conf_dist.get('low (<0.7)', 0)
                ])
            else:
                row.extend([0, 0, 0, 0, 0, 0, 0, 0])
            
            perf = result['performance']
            row.extend([
                perf.get('elapsed_time_seconds', 0),
                perf.get('elapsed_time_ms', 0)
            ])
            
            if PSUTIL_AVAILABLE:
                row.extend([
                    perf.get('peak_memory_mb', 0),
                    perf.get('memory_increase_mb', 0)
                ])
            
            writer.writerow(row)
    
    print(f"✓ CSV export saved: {csv_file}")


def main():
    """Main benchmark function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Benchmark PaddleOCR for Nanonets comparison',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--input', '-i', 
                        default='test_documents/nanonets_comparison',
                        help='Input directory with extracted page images')
    parser.add_argument('--output', '-o',
                        default='test_results/nanonets_comparison',
                        help='Output directory for results')
    
    args = parser.parse_args()
    
    # Run benchmark
    summary = benchmark_all_pages(args.input, args.output)
    
    if summary:
        print("\n" + "="*70)
        print("✓ Benchmark completed successfully!")
        print("="*70)
        print("\nGenerated files:")
        print(f"  - {args.output}/nanonets_comparison_results.json")
        print(f"  - {args.output}/NANONETS_COMPARISON_REPORT.md")
        print(f"  - {args.output}/performance_metrics.csv")
        print(f"  - Individual page results (JSON, TXT, annotated images)")
        print("\n" + "="*70)
        print("Next Steps:")
        print("="*70)
        print("1. Share the extracted page images with your colleagues")
        print("2. Have them run the same pages through Nanonets")
        print("3. Fill in the comparison table in NANONETS_COMPARISON_REPORT.md")
        print("4. Compare the results!")


if __name__ == "__main__":
    main()

