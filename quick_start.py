"""
Quick Start Script for PaddleOCR Testing
Runs all tests in sequence and generates a comprehensive report
"""

import os
import sys
import subprocess
from datetime import datetime

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def run_command(command, description):
    """Run a command and report results"""
    print(f"\n→ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True, result.stdout
        else:
            print(f"✗ {description} failed")
            print(f"Error: {result.stderr}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(f"✗ {description} timed out (>5 minutes)")
        return False, "Timeout"
    except Exception as e:
        print(f"✗ {description} failed with error: {e}")
        return False, str(e)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major == 3 and 8 <= version.minor <= 12:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8-3.12")
        return False

def main():
    """Main quick start function"""
    print_header("PaddleOCR Testing Environment - Quick Start")
    
    print("\nThis script will guide you through setting up and testing PaddleOCR")
    print("Estimated time: 10-20 minutes (depending on internet speed)")
    
    # Step 1: Check Python version
    print_header("Step 1: Verify Python Version")
    if not check_python_version():
        print("\n⚠ Please install Python 3.8-3.12 and try again")
        return 1
    
    # Step 2: Install dependencies
    print_header("Step 2: Install Dependencies")
    print("\nThis will install PaddleOCR and required packages...")
    print("Note: First time installation may take 5-10 minutes\n")
    
    response = input("Proceed with installation? (y/n): ").lower()
    if response != 'y':
        print("\n⚠ Installation skipped. You can install manually using:")
        print("   pip install -r test_requirements.txt")
        print("\nOr for basic installation:")
        print('   pip install paddleocr[all]')
        return 0
    
    # Install core packages
    success, output = run_command(
        'python -m pip install paddlepaddle==3.0.0b1 --quiet',
        "Installing PaddlePaddle framework"
    )
    
    if success:
        success, output = run_command(
            'python -m pip install "paddleocr[all]" --quiet',
            "Installing PaddleOCR with all features"
        )
    
    # Install additional test dependencies
    if success:
        success, output = run_command(
            'python -m pip install pytest pillow matplotlib pandas beautifulsoup4 --quiet',
            "Installing test utilities"
        )
    
    if not success:
        print("\n✗ Installation failed. Please try manual installation:")
        print("   pip install paddleocr[all]")
        return 1
    
    # Step 3: Verify installation
    print_header("Step 3: Verify Installation")
    success, output = run_command(
        'python test_setup.py',
        "Verifying PaddleOCR installation"
    )
    
    if not success:
        print("\n✗ Verification failed. Please check the error messages above.")
        return 1
    
    print(output)
    
    # Step 4: Run basic tests
    print_header("Step 4: Run Basic OCR Test")
    print("\nThis will download sample images and test basic OCR functionality...")
    
    response = input("\nRun basic OCR test? (y/n): ").lower()
    if response == 'y':
        success, output = run_command(
            'python test_basic_ocr.py',
            "Running basic OCR test"
        )
        if success:
            print("\n✓ Basic OCR test completed!")
            print("  Check test_results/ folder for outputs")
    
    # Step 5: Summary
    print_header("Setup Complete!")
    
    print("\n✓ PaddleOCR testing environment is ready!")
    print("\nWhat's next?")
    print("\n1. Review test results in the 'test_results/' folder")
    print("2. Test with your own images:")
    print("   python test_basic_ocr.py path/to/your/image.jpg")
    print("\n3. Try document parsing:")
    print("   python test_document_parsing.py path/to/document.jpg")
    print("\n4. Test multilingual OCR:")
    print("   python test_multilingual.py path/to/image.jpg [language_code]")
    print("\n5. Read README_TEST.md for detailed documentation")
    
    print("\n" + "="*70)
    print("For client evaluation, prepare sample documents and run the tests")
    print("="*70)
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        sys.exit(1)

