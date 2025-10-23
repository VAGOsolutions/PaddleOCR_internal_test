#!/bin/bash
# PaddleOCR Testing Environment Setup for Linux/WSL
# This script handles various Python environment managers

set -e  # Exit on error

echo "======================================================================"
echo "  PaddleOCR Testing Environment Setup"
echo "======================================================================"

# Check Python version
echo ""
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"

# Detect environment manager
echo ""
echo "Detecting package manager..."

if command -v uv &> /dev/null; then
    echo "✓ Found 'uv' package manager"
    MANAGER="uv"
elif command -v pip3 &> /dev/null; then
    echo "✓ Found 'pip3'"
    MANAGER="pip3"
elif command -v pip &> /dev/null; then
    echo "✓ Found 'pip'"
    MANAGER="pip"
else
    echo "✗ No package manager found. Installing pip..."
    sudo apt update && sudo apt install -y python3-pip
    MANAGER="pip3"
fi

echo ""
echo "======================================================================"
echo "  Installing PaddleOCR Dependencies"
echo "======================================================================"
echo "This will install:"
echo "  - PaddlePaddle framework"
echo "  - PaddleOCR with all features"
echo "  - Testing utilities"
echo ""
echo "Estimated time: 5-10 minutes"
echo ""

read -p "Proceed with installation? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 0
fi

echo ""
echo "→ Installing PaddlePaddle framework..."
if [ "$MANAGER" = "uv" ]; then
    uv pip install paddlepaddle==3.0.0b1
elif [ "$MANAGER" = "pip3" ]; then
    pip3 install paddlepaddle==3.0.0b1
else
    pip install paddlepaddle==3.0.0b1
fi
echo "✓ PaddlePaddle installed"

echo ""
echo "→ Installing PaddleOCR with all features..."
if [ "$MANAGER" = "uv" ]; then
    uv pip install "paddleocr[all]"
elif [ "$MANAGER" = "pip3" ]; then
    pip3 install "paddleocr[all]"
else
    pip install "paddleocr[all]"
fi
echo "✓ PaddleOCR installed"

echo ""
echo "→ Installing testing utilities..."
if [ "$MANAGER" = "uv" ]; then
    uv pip install pytest pillow matplotlib pandas beautifulsoup4
elif [ "$MANAGER" = "pip3" ]; then
    pip3 install pytest pillow matplotlib pandas beautifulsoup4
else
    pip install pytest pillow matplotlib pandas beautifulsoup4
fi
echo "✓ Testing utilities installed"

echo ""
echo "======================================================================"
echo "  Verifying Installation"
echo "======================================================================"
echo ""

# Run verification
if [ "$MANAGER" = "uv" ]; then
    uv run python test_setup.py
else
    python3 test_setup.py
fi

echo ""
echo "======================================================================"
echo "  Installation Complete!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo "1. Run basic OCR test:"
if [ "$MANAGER" = "uv" ]; then
    echo "   uv run python test_basic_ocr.py"
else
    echo "   python3 test_basic_ocr.py"
fi
echo ""
echo "2. Test with your own image:"
if [ "$MANAGER" = "uv" ]; then
    echo "   uv run python test_basic_ocr.py path/to/image.jpg"
else
    echo "   python3 test_basic_ocr.py path/to/image.jpg"
fi
echo ""
echo "3. Read documentation:"
echo "   cat README_TEST.md"
echo ""
echo "======================================================================"

