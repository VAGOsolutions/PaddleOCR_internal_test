# PaddleOCR Installation Guide

## 🚨 Quick Fix for Current Issue

You're seeing an error because your virtual environment doesn't have `pip` installed. Here's how to fix it:

### Solution A: Use uv (Recommended if you're using uv)

```bash
# Install dependencies using uv
uv pip install paddlepaddle==3.0.0b1
uv pip install "paddleocr[all]"
uv pip install pytest pillow matplotlib pandas beautifulsoup4

# Verify installation
uv run python test_setup.py

# Run tests
uv run python test_basic_ocr.py
```

### Solution B: Use the automated setup script

```bash
# Make the script executable
chmod +x setup_env.sh

# Run the setup script
./setup_env.sh
```

### Solution C: Recreate virtual environment with proper pip

```bash
# Deactivate current environment
deactivate

# Remove broken venv
rm -rf .venv

# Create new venv with pip
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r test_requirements.txt

# Verify
python test_setup.py
```

## 📋 Detailed Installation Instructions

### For Windows Subsystem for Linux (WSL)

Your current environment (detected from terminal):
- ✅ WSL/Linux
- ✅ Python 3.12.3
- ✅ Using `uv` package manager

**Recommended approach:**

```bash
# Option 1: Install with uv (fastest)
uv pip install paddlepaddle==3.0.0b1
uv pip install "paddleocr[all]"

# Test it
uv run python test_basic_ocr.py
```

```bash
# Option 2: Use system Python
pip3 install paddlepaddle==3.0.0b1
pip3 install "paddleocr[all]"

# Test it
python3 test_basic_ocr.py
```

### For Native Linux

```bash
# Install pip if needed
sudo apt update
sudo apt install python3-pip python3-venv

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r test_requirements.txt

# Verify
python test_setup.py
```

### For Windows (Native)

```powershell
# In PowerShell
python -m pip install paddlepaddle==3.0.0b1
python -m pip install "paddleocr[all]"

# Verify
python test_setup.py
```

### For macOS

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r test_requirements.txt

# Verify
python test_setup.py
```

## 🔧 Troubleshooting

### Issue: "No module named pip"

**Cause**: Virtual environment created without pip (common with `uv`)

**Fix**:
```bash
# Use uv's pip
uv pip install <package>

# OR recreate venv properly
python3 -m venv --clear .venv
```

### Issue: "Could not find a version that satisfies the requirement"

**Cause**: Wrong Python version or architecture

**Fix**:
```bash
# Check Python version (must be 3.8-3.12)
python3 --version

# Update pip
python3 -m pip install --upgrade pip
```

### Issue: Installation is slow

**Cause**: Large packages being downloaded

**Solutions**:
- Use a faster internet connection
- Use mirrors: `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple paddleocr[all]`
- Be patient (first install takes 5-10 minutes)

### Issue: "CUDA not available"

**Cause**: This is normal if you don't have an NVIDIA GPU

**Fix**: 
- For CPU-only use: This is fine, PaddleOCR works on CPU
- For GPU: Install CUDA-enabled PaddlePaddle:
  ```bash
  pip install paddlepaddle-gpu==3.0.0b1
  ```

### Issue: Import errors after installation

**Fix**:
```bash
# Verify installation
python3 -c "import paddleocr; print(paddleocr.__version__)"

# Reinstall if needed
pip uninstall paddleocr paddlepaddle
pip install paddlepaddle==3.0.0b1
pip install "paddleocr[all]"
```

## 📦 Package Versions

For reference, here are the key packages:

```
paddlepaddle==3.0.0b1          # Core framework
paddleocr[all]>=3.3.0          # OCR toolkit with all features
pillow>=9.0.0                  # Image processing
opencv-python>=4.5.0           # Computer vision
numpy>=1.21.0                  # Numerical computing
pandas>=1.3.0                  # Data processing
matplotlib>=3.5.0              # Visualization
beautifulsoup4                 # HTML parsing (for tables)
pytest>=7.0.0                  # Testing framework
```

## 🚀 Quick Verification

After installation, run:

```bash
# If using uv
uv run python test_setup.py

# If using regular Python
python3 test_setup.py
```

You should see:
```
✓ PaddlePaddle version: 3.0.0b1
✓ PaddleOCR version: 3.3.0
✓ CUDA available: False (or True)
✓ PIL is installed
✓ cv2 is installed
✓ numpy is installed
✓ matplotlib is installed
```

## 🎯 Next Steps After Installation

1. **Verify everything works:**
   ```bash
   python3 test_setup.py
   ```

2. **Run basic OCR test:**
   ```bash
   python3 test_basic_ocr.py
   ```

3. **Test with your own image:**
   ```bash
   python3 test_basic_ocr.py path/to/your/image.jpg
   ```

4. **Read the documentation:**
   - Technical details: `README_TEST.md`
   - Business case: `CLIENT_EVALUATION_GUIDE.md`
   - Quick overview: `PROJECT_OVERVIEW.md`

## 💡 Pro Tips

### Using uv (Modern Python Package Manager)

If you're using `uv`, always prefix commands with `uv run`:
```bash
uv run python test_basic_ocr.py
uv run python test_document_parsing.py
```

### GPU Acceleration

For faster processing with NVIDIA GPU:
```bash
# Install GPU version
pip install paddlepaddle-gpu==3.0.0b1

# Verify CUDA is available
python3 -c "import paddle; print(paddle.device.is_compiled_with_cuda())"
```

### Virtual Environment Best Practices

```bash
# Always activate before use
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Deactivate when done
deactivate
```

### Testing Without Installation

You can test PaddleOCR in Colab without local installation:
- Open [Google Colab](https://colab.research.google.com/)
- Copy test scripts
- Run in cloud

## 📞 Need Help?

If installation still fails:

1. Check system requirements:
   - Python 3.8-3.12
   - 8GB+ RAM recommended
   - Internet connection for model downloads

2. Try manual installation:
   ```bash
   pip3 install paddleocr
   ```

3. Check official docs:
   - https://github.com/PaddlePaddle/PaddleOCR
   - https://paddlepaddle.github.io/PaddleOCR/

4. Review error messages and search GitHub issues:
   - https://github.com/PaddlePaddle/PaddleOCR/issues

---

**Current Status**: Ready to install ✅
**Recommended Command**: `./setup_env.sh` or use the Solutions A/B/C above

