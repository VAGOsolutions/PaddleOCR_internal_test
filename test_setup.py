"""
PaddleOCR Testing Environment Setup Script
This script verifies the installation and basic functionality of PaddleOCR
"""

import sys
import subprocess

def check_installation():
    """Check if PaddleOCR is properly installed"""
    try:
        import paddleocr
        print(f"✓ PaddleOCR version: {paddleocr.__version__}")
        return True
    except ImportError as e:
        print(f"✗ PaddleOCR not installed: {e}")
        return False

def check_paddle():
    """Check if PaddlePaddle is properly installed"""
    try:
        import paddle
        print(f"✓ PaddlePaddle version: {paddle.__version__}")
        print(f"✓ CUDA available: {paddle.device.is_compiled_with_cuda()}")
        if paddle.device.is_compiled_with_cuda():
            print(f"✓ GPU count: {paddle.device.cuda.device_count()}")
        return True
    except ImportError as e:
        print(f"✗ PaddlePaddle not installed: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    dependencies = ['PIL', 'cv2', 'numpy', 'matplotlib']
    all_installed = True
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} is installed")
        except ImportError:
            print(f"✗ {dep} is not installed")
            all_installed = False
    
    return all_installed

def main():
    """Main setup verification"""
    print("=" * 60)
    print("PaddleOCR Testing Environment Verification")
    print("=" * 60)
    
    paddle_ok = check_paddle()
    paddleocr_ok = check_installation()
    deps_ok = check_dependencies()
    
    print("\n" + "=" * 60)
    if paddle_ok and paddleocr_ok and deps_ok:
        print("✓ All checks passed! Environment is ready for testing.")
        return 0
    else:
        print("✗ Some checks failed. Please install missing dependencies.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

