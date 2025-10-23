"""
Multilingual OCR Testing Script for PaddleOCR
Tests OCR capabilities across different languages
"""

import os
import sys
import json
from datetime import datetime

def test_multilingual_ocr(image_path, language='en', output_dir="test_results/multilingual"):
    """
    Test multilingual OCR functionality
    
    Args:
        image_path: Path to the test image
        language: Language code (en, ch, fr, german, korean, japan, etc.)
        output_dir: Directory to save results
    """
    try:
        from paddleocr import PaddleOCR
        
        print("\n" + "="*60)
        print(f"Testing Multilingual OCR - Language: {language}")
        print("="*60)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize PaddleOCR with specified language
        print(f"\nInitializing PaddleOCR for {language}...")
        ocr = PaddleOCR(
            use_textline_orientation=True,
            lang=language
        )
        
        if not os.path.exists(image_path):
            print(f"✗ Image not found: {image_path}")
            return False
        
        print(f"✓ Processing image: {image_path}")
        
        # Perform OCR
        result = ocr.predict(image_path)
        
        # Process results
        if result and result[0]:
            print(f"✓ Found {len(result[0])} text regions\n")
            
            # Save results
            output_data = {
                "timestamp": datetime.now().isoformat(),
                "language": language,
                "image_path": str(image_path),
                "total_regions": len(result[0]),
                "results": []
            }
            
            print("Detected Text:")
            print("-" * 60)
            for idx, line in enumerate(result[0], 1):
                # Handle different result formats
                if isinstance(line, dict):
                    text = line.get('text', '')
                    confidence = line.get('score', 0.0)
                    box = line.get('bbox', [])
                elif isinstance(line, (list, tuple)) and len(line) >= 2:
                    box = line[0]
                    if isinstance(line[1], (list, tuple)) and len(line[1]) >= 2:
                        text = line[1][0]
                        confidence = line[1][1]
                    else:
                        text = str(line[1])
                        confidence = 0.0
                else:
                    continue
                
                print(f"{idx}. {text} (confidence: {confidence:.4f})")
                
                output_data["results"].append({
                    "index": idx,
                    "text": text,
                    "confidence": float(confidence),
                    "box": box if isinstance(box, list) else []
                })
            
            # Save results
            result_file = os.path.join(output_dir, f"ocr_results_{language}.json")
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Results saved to: {result_file}")
            
            return True
        else:
            print("✗ No text detected in the image")
            return False
            
    except Exception as e:
        print(f"✗ Error during OCR: {e}")
        import traceback
        traceback.print_exc()
        return False


def list_supported_languages():
    """List all supported languages in PaddleOCR"""
    languages = {
        'ch': 'Chinese & English',
        'en': 'English',
        'french': 'French',
        'german': 'German',
        'korean': 'Korean',
        'japan': 'Japanese',
        'chinese_cht': 'Traditional Chinese',
        'it': 'Italian',
        'es': 'Spanish',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'ug': 'Uyghur',
        'fa': 'Persian',
        'ur': 'Urdu',
        'rs_latin': 'Serbian (Latin)',
        'oc': 'Occitan',
        'mr': 'Marathi',
        'ne': 'Nepali',
        'rsc': 'Serbian (Cyrillic)',
        'bg': 'Bulgarian',
        'uk': 'Ukrainian',
        'be': 'Belarusian',
        'te': 'Telugu',
        'kn': 'Kannada',
        'ta': 'Tamil',
        'af': 'Afrikaans',
        'az': 'Azerbaijani',
        'bs': 'Bosnian',
        'cs': 'Czech',
        'cy': 'Welsh',
        'da': 'Danish',
        'et': 'Estonian',
        'ga': 'Irish',
        'hr': 'Croatian',
        'hu': 'Hungarian',
        'id': 'Indonesian',
        'is': 'Icelandic',
        'ku': 'Kurdish',
        'lt': 'Lithuanian',
        'lv': 'Latvian',
        'mi': 'Maori',
        'ms': 'Malay',
        'mt': 'Maltese',
        'nl': 'Dutch',
        'no': 'Norwegian',
        'pl': 'Polish',
        'ro': 'Romanian',
        'sk': 'Slovak',
        'sl': 'Slovenian',
        'sq': 'Albanian',
        'sv': 'Swedish',
        'sw': 'Swahili',
        'tl': 'Tagalog',
        'tr': 'Turkish',
        'uz': 'Uzbek',
        'vi': 'Vietnamese',
    }
    
    print("\n" + "="*60)
    print("Supported Languages in PaddleOCR (100+ languages)")
    print("="*60)
    print("\nMain Languages:")
    main_langs = ['ch', 'en', 'french', 'german', 'korean', 'japan', 'chinese_cht', 
                  'it', 'es', 'pt', 'ru', 'ar', 'hi']
    for lang in main_langs:
        print(f"  {lang:15} - {languages[lang]}")
    
    print("\nTo see the full list of 100+ supported languages, visit:")
    print("https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_en/multi_languages_en.md")


def main():
    """Main testing function"""
    print("="*60)
    print("PaddleOCR Multilingual Testing Suite")
    print("="*60)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--list-languages':
            list_supported_languages()
        else:
            image_path = sys.argv[1]
            language = sys.argv[2] if len(sys.argv) > 2 else 'en'
            test_multilingual_ocr(image_path, language)
    else:
        print("\nUsage:")
        print("  python test_multilingual.py <image_path> [language_code]")
        print("  python test_multilingual.py --list-languages")
        print("\nExamples:")
        print("  python test_multilingual.py document.jpg en")
        print("  python test_multilingual.py chinese_doc.jpg ch")
        print("  python test_multilingual.py french_text.jpg french")
        list_supported_languages()


if __name__ == "__main__":
    main()

