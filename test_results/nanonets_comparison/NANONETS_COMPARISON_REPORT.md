# OCR Benchmark Results - PaddleOCR vs Nanonets

**Test Date:** 2025-10-27 19:25:07  
**Document:** IBM Cloud Foundations Benchmark v1.1.0  
**Pages Tested:** 10  

---

## PaddleOCR Results

### Overview

- **OCR Engine:** PaddleOCR v3.3.0 (PP-OCRv5)
- **Total Pages:** 10
- **Successfully Processed:** 10
- **Failed:** 0
- **Success Rate:** 100.0%

### Accuracy Metrics

- **Total Text Regions Detected:** 453
- **Total Characters Extracted:** 12861
- **Average Confidence Score:** 0.9799 (97.99%)
- **Average Regions per Page:** 45.3
- **Average Characters per Page:** 1286.1

### Performance Metrics

- **Total Processing Time:** 535.39 seconds
- **Average Time per Page:** 53.5394s (53539.43ms)
- **Peak Memory Usage:** 1951.94 MB

### Per-Page Results

| Page | Text Regions | Characters | Avg Confidence | Time (ms) | Status |
|------|--------------|------------|----------------|-----------|--------|
| page_003.png | 76 | 1348 | 0.9762 | 47731.72 | ✅ |
| page_052.png | 43 | 1210 | 0.9931 | 45924.81 | ✅ |
| page_058.png | 37 | 1489 | 0.9888 | 49500.50 | ✅ |
| page_117.png | 41 | 1487 | 0.9860 | 52076.01 | ✅ |
| page_138.png | 45 | 1477 | 0.9139 | 67655.77 | ✅ |
| page_143.png | 57 | 1760 | 0.9889 | 53698.81 | ✅ |
| page_183.png | 42 | 1560 | 0.9732 | 48827.94 | ✅ |
| page_228.png | 47 | 1085 | 0.9932 | 47821.32 | ✅ |
| page_229.png | 47 | 1099 | 0.9921 | 51027.98 | ✅ |
| page_255.png | 18 | 346 | 0.9935 | 52470.61 | ✅ |

---

## Side-by-Side Comparison

Use this table to add Nanonets results for comparison:

| Metric | PaddleOCR | Nanonets | Winner |
|--------|-----------|----------|--------|
| **Total Processing Time (s)** | 535.39 | _[Add result]_ | |
| **Avg Time per Page (ms)** | 53539.43 | _[Add result]_ | |
| **Avg Confidence Score** | 0.9799 | _[Add result]_ | |
| **Total Text Regions** | 453 | _[Add result]_ | |
| **Total Characters** | 12861 | _[Add result]_ | |
| **Success Rate** | 10/10 | _[Add result]_ | |
| **Peak Memory (MB)** | 1951.94 | _[Add result]_ | |

### Notes

- All times measured on the same hardware
- Pages selected for complexity (tables, dense text, technical content)
- Confidence scores range from 0.0 to 1.0

---

*Generated automatically by PaddleOCR benchmark script*
