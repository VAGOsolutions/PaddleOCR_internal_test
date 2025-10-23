# PaddleOCR Test Results - Model Comparison Ready

**Test Date:** 2025-10-23 22:06:05  
**Model:** PaddleOCR v3.3.0 (PP-OCRv5)  
**Total Documents:** 9  

## Summary Statistics

- **Success Rate:** 9/9 (100.0%)
- **Total Processing Time:** 342.31s
- **Average Time per Document:** 38.03s

## Detailed Results by Document

| Category | Document | Text Regions | Avg Confidence | Time (s) | Status |
|----------|----------|--------------|----------------|----------|--------|
| tables | sales_report.jpg | 39 | 0.9941 | 36.79 | ✅ |
| tables | table_sample_1.jpg | 71 | 0.9907 | 15.06 | ✅ |
| invoices | sample_invoice.jpg | 38 | 0.9878 | 20.99 | ✅ |
| forms | form_sample_1.jpg | 153 | 0.4432 | 132.71 | ✅ |
| forms | registration_form.jpg | 28 | 0.9844 | 28.19 | ✅ |
| papers | computer_vision_paper.jpg | 36 | 0.9851 | 24.34 | ✅ |
| papers | conference_paper.jpg | 28 | 0.9853 | 22.84 | ✅ |
| papers | nlp_survey_paper.jpg | 68 | 0.9871 | 26.40 | ✅ |
| mixed | complex_layout.jpg | 71 | 0.9967 | 34.99 | ✅ |

## Results by Category

| Category | Documents | Success Rate | Avg Regions | Avg Confidence | Avg Time (s) |
|----------|-----------|--------------|-------------|----------------|-------------|
| forms | 2 | 100% | 90 | 0.7138 | 80.45 |
| invoices | 1 | 100% | 38 | 0.9878 | 20.99 |
| mixed | 1 | 100% | 71 | 0.9967 | 34.99 |
| papers | 3 | 100% | 44 | 0.9858 | 24.53 |
| tables | 2 | 100% | 55 | 0.9924 | 25.93 |

## Model Comparison Template

Use this table to compare with other OCR models:

| Model | Total Time (s) | Avg Time (s) | Avg Confidence | Success Rate | Notes |
|-------|----------------|--------------|----------------|--------------|-------|
| **PaddleOCR v3.3.0** | 342.31 | 38.03 | 0.9283 | 9/9 | Baseline |
| Tesseract | - | - | - | - | Add results |
| EasyOCR | - | - | - | - | Add results |
| Other Model | - | - | - | - | Add results |

---

**Ready for comparison testing with other OCR models.**
