"""
Create sample research paper documents for PaddleOCR testing
Generates academic paper layouts with titles, abstracts, columns, etc.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_research_paper_1():
    """Create a simple research paper layout"""
    width, height = 850, 1100
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_author = ImageFont.truetype("arial.ttf", 14)
        font_section = ImageFont.truetype("arialbd.ttf", 16)
        font_text = ImageFont.truetype("arial.ttf", 12)
    except:
        font_title = font_author = font_section = font_text = ImageFont.load_default()
    
    y = 40
    
    # Title
    title = "Deep Learning for Natural Language Processing:"
    subtitle = "A Comprehensive Survey"
    draw.text((100, y), title, fill='black', font=font_title)
    y += 35
    draw.text((200, y), subtitle, fill='black', font=font_title)
    y += 50
    
    # Authors
    authors = "John Smith¹, Jane Doe², Robert Johnson³"
    draw.text((200, y), authors, fill='black', font=font_author)
    y += 25
    
    affiliations = [
        "¹Department of Computer Science, MIT",
        "²AI Research Lab, Stanford University",
        "³Google Research, Mountain View, CA"
    ]
    for aff in affiliations:
        draw.text((150, y), aff, fill='gray', font=font_text)
        y += 20
    
    y += 20
    
    # Abstract
    draw.text((50, y), "Abstract", fill='black', font=font_section)
    y += 25
    
    abstract_text = [
        "Natural Language Processing (NLP) has witnessed remarkable progress",
        "in recent years, driven by advances in deep learning architectures.",
        "This paper provides a comprehensive survey of state-of-the-art",
        "techniques, including transformer models, attention mechanisms, and",
        "pre-trained language models. We analyze their applications across",
        "various NLP tasks and discuss future research directions."
    ]
    
    for line in abstract_text:
        draw.text((70, y), line, fill='black', font=font_text)
        y += 18
    
    y += 30
    
    # Two-column layout
    col1_x = 50
    col2_x = 450
    col_width = 350
    
    # Section 1
    draw.text((col1_x, y), "1. Introduction", fill='black', font=font_section)
    y += 25
    
    intro_text = [
        "Deep learning has revolutionized",
        "the field of natural language",
        "processing. Recent advances in",
        "neural network architectures",
        "have enabled machines to",
        "understand and generate human",
        "language with unprecedented",
        "accuracy.",
        "",
        "The introduction of attention",
        "mechanisms and transformer",
        "models has been particularly",
        "impactful. These innovations",
        "have led to breakthrough",
        "results across multiple NLP",
        "benchmarks."
    ]
    
    temp_y = y
    for line in intro_text:
        draw.text((col1_x + 20, temp_y), line, fill='black', font=font_text)
        temp_y += 16
    
    # Section 2 in second column
    draw.text((col2_x, y), "2. Related Work", fill='black', font=font_section)
    y += 25
    
    related_text = [
        "Traditional NLP approaches",
        "relied heavily on hand-crafted",
        "features and linguistic rules.",
        "The shift to deep learning",
        "began with word embeddings",
        "and recurrent neural networks.",
        "",
        "Key milestones include:",
        "• Word2Vec (2013)",
        "• LSTM networks (2014)",
        "• Attention mechanism (2015)",
        "• Transformer (2017)",
        "• BERT (2018)",
        "• GPT series (2018-2023)"
    ]
    
    temp_y = y
    for line in related_text:
        draw.text((col2_x + 20, temp_y), line, fill='black', font=font_text)
        temp_y += 16
    
    # Continue with more sections
    y = temp_y + 30
    
    # Section 3
    draw.text((col1_x, y), "3. Methodology", fill='black', font=font_section)
    y += 25
    
    method_text = [
        "Our approach combines several",
        "key components:",
        "",
        "3.1 Model Architecture",
        "We employ a transformer-based",
        "encoder-decoder architecture",
        "with multi-head attention.",
        "",
        "3.2 Training Procedure", 
        "The model is pre-trained on",
        "large text corpora using",
        "masked language modeling."
    ]
    
    temp_y = y
    for line in method_text:
        draw.text((col1_x + 20, temp_y), line, fill='black', font=font_text)
        temp_y += 16
    
    # Section 4
    draw.text((col2_x, y), "4. Results", fill='black', font=font_section)
    y += 25
    
    results_text = [
        "Table 1 shows performance",
        "on standard benchmarks:",
        "",
        "Task        Accuracy",
        "-------------------------",
        "GLUE        92.3%",
        "SQuAD       91.5%",
        "CoNLL       94.2%",
        "",
        "Our model achieves state-of-",
        "the-art results, outperforming",
        "previous approaches by 2-3%."
    ]
    
    temp_y = y
    for line in results_text:
        draw.text((col2_x + 20, temp_y), line, fill='black', font=font_text)
        temp_y += 16
    
    # Footer
    y = height - 40
    draw.text((50, y), "Proceedings of ICML 2025", fill='gray', font=font_text)
    draw.text((width - 150, y), "Page 1 of 10", fill='gray', font=font_text)
    
    return img

def create_research_paper_2():
    """Create another research paper with different layout"""
    width, height = 850, 1100
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 22)
        font_section = ImageFont.truetype("arialbd.ttf", 14)
        font_text = ImageFont.truetype("arial.ttf", 11)
    except:
        font_title = font_section = font_text = ImageFont.load_default()
    
    y = 50
    
    # Title
    title1 = "Advances in Computer Vision:"
    title2 = "From CNNs to Vision Transformers"
    draw.text((120, y), title1, fill='black', font=font_title)
    y += 30
    draw.text((150, y), title2, fill='black', font=font_title)
    y += 50
    
    # Authors
    draw.text((250, y), "Alice Chen · Bob Wilson · Carol Davis", fill='black', font=font_text)
    y += 20
    draw.text((280, y), "University of California, Berkeley", fill='gray', font=font_text)
    y += 40
    
    # Abstract box
    draw.rectangle([(40, y), (810, y + 140)], outline='black', width=1)
    y += 10
    draw.text((50, y), "ABSTRACT", fill='black', font=font_section)
    y += 25
    
    abstract = [
        "Computer vision has evolved dramatically with deep learning. This paper",
        "reviews the progression from convolutional neural networks to modern",
        "vision transformers. We analyze architectural innovations, training",
        "techniques, and performance improvements across image classification,",
        "object detection, and segmentation tasks. Our experiments demonstrate",
        "that hybrid approaches combining CNNs and transformers achieve optimal",
        "results for most vision tasks."
    ]
    
    for line in abstract:
        draw.text((60, y), line, fill='black', font=font_text)
        y += 16
    
    y += 40
    
    # Single column content
    sections = [
        ("1. INTRODUCTION", [
            "Deep learning has transformed computer vision since AlexNet's",
            "breakthrough in 2012. Convolutional Neural Networks (CNNs) became",
            "the dominant architecture for image-related tasks.",
            "",
            "Recent introduction of Vision Transformers (ViT) challenges this",
            "paradigm, showing that attention-based models can match or exceed",
            "CNN performance when trained on sufficient data."
        ]),
        ("2. BACKGROUND", [
            "2.1 Convolutional Neural Networks",
            "CNNs use local receptive fields and parameter sharing to process",
            "images efficiently. Key architectures include ResNet, VGG, and",
            "Inception networks.",
            "",
            "2.2 Vision Transformers",
            "ViT applies transformer architecture to image patches. Self-attention",
            "mechanisms capture global dependencies without convolutions."
        ]),
        ("3. EXPERIMENTAL SETUP", [
            "We evaluate models on ImageNet-1K (1.3M images, 1000 classes).",
            "Training uses standard data augmentation: random crops, flips,",
            "and color jittering. All models trained for 300 epochs with",
            "AdamW optimizer."
        ])
    ]
    
    for section_title, section_text in sections:
        draw.text((50, y), section_title, fill='black', font=font_section)
        y += 25
        
        for line in section_text:
            if line:
                draw.text((70, y), line, fill='black', font=font_text)
            y += 16
        
        y += 10
    
    # References
    y += 20
    draw.text((50, y), "REFERENCES", fill='black', font=font_section)
    y += 25
    
    refs = [
        "[1] He et al. Deep Residual Learning. CVPR 2016.",
        "[2] Dosovitskiy et al. An Image is Worth 16x16 Words. ICLR 2021.",
        "[3] Liu et al. Swin Transformer. ICCV 2021."
    ]
    
    for ref in refs:
        draw.text((70, y), ref, fill='black', font=font_text)
        y += 18
    
    return img

def create_conference_paper():
    """Create a conference paper format"""
    width, height = 850, 1100
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_conf = ImageFont.truetype("arial.ttf", 10)
        font_title = ImageFont.truetype("arialbd.ttf", 20)
        font_text = ImageFont.truetype("arial.ttf", 11)
    except:
        font_conf = font_title = font_text = ImageFont.load_default()
    
    # Header
    draw.rectangle([(0, 0), (width, 30)], fill='lightgray')
    draw.text((30, 8), "NeurIPS 2025 - Neural Information Processing Systems", fill='black', font=font_conf)
    
    y = 50
    
    # Title
    title = "Efficient Training of Large Language Models"
    draw.text((150, y), title, fill='black', font=font_title)
    y += 35
    
    subtitle = "Using Mixed Precision and Gradient Checkpointing"
    draw.text((180, y), subtitle, fill='black', font=font_title)
    y += 60
    
    # Two columns
    col1_x, col2_x = 50, 450
    
    # Column 1
    temp_y = y
    draw.text((col1_x, temp_y), "ABSTRACT", fill='black', font=font_text)
    temp_y += 20
    
    abstract_col1 = [
        "Training large language models",
        "requires substantial computational",
        "resources. We propose techniques",
        "to reduce memory footprint and",
        "training time while maintaining",
        "model quality. Our approach",
        "combines mixed precision training",
        "with gradient checkpointing."
    ]
    
    for line in abstract_col1:
        draw.text((col1_x, temp_y), line, fill='black', font=font_text)
        temp_y += 15
    
    temp_y += 20
    draw.text((col1_x, temp_y), "1. MOTIVATION", fill='black', font=font_text)
    temp_y += 20
    
    motiv = [
        "Modern LLMs have billions of",
        "parameters. Standard training",
        "methods are prohibitively",
        "expensive for most researchers.",
        "Memory requirements often exceed",
        "available GPU capacity."
    ]
    
    for line in motiv:
        draw.text((col1_x + 10, temp_y), line, fill='black', font=font_text)
        temp_y += 15
    
    # Column 2
    temp_y = y
    draw.text((col2_x, temp_y), "KEYWORDS", fill='black', font=font_text)
    temp_y += 20
    
    keywords = [
        "Large Language Models",
        "Mixed Precision Training",
        "Gradient Checkpointing",
        "Memory Optimization"
    ]
    
    for kw in keywords:
        draw.text((col2_x, temp_y), f"• {kw}", fill='black', font=font_text)
        temp_y += 15
    
    temp_y += 20
    draw.text((col2_x, temp_y), "2. CONTRIBUTIONS", fill='black', font=font_text)
    temp_y += 20
    
    contrib = [
        "• 40% reduction in memory usage",
        "• 2x faster training",
        "• No loss in model quality",
        "• Open-source implementation"
    ]
    
    for line in contrib:
        draw.text((col2_x + 10, temp_y), line, fill='black', font=font_text)
        temp_y += 15
    
    # Footer
    draw.line([(30, height - 50), (width - 30, height - 50)], fill='gray', width=1)
    draw.text((350, height - 35), "Page 1", fill='gray', font=font_conf)
    
    return img

def main():
    """Create all research paper samples"""
    print("="*60)
    print("Creating Research Paper Samples")
    print("="*60)
    
    os.makedirs("test_documents/papers", exist_ok=True)
    
    papers = [
        (create_research_paper_1, "test_documents/papers/nlp_survey_paper.jpg", "NLP Survey Paper"),
        (create_research_paper_2, "test_documents/papers/computer_vision_paper.jpg", "Computer Vision Paper"),
        (create_conference_paper, "test_documents/papers/conference_paper.jpg", "Conference Paper")
    ]
    
    print("\nCreating papers...")
    for create_func, filepath, description in papers:
        try:
            img = create_func()
            img.save(filepath, quality=95)
            print(f"✓ Created: {description} -> {filepath}")
        except Exception as e:
            print(f"✗ Failed to create {description}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("Research papers created successfully!")
    print("="*60)
    print("\nTest these papers with:")
    print("  python test_basic_ocr.py test_documents\\papers\\nlp_survey_paper.jpg")
    print("  python test_basic_ocr.py test_documents\\papers\\computer_vision_paper.jpg")
    print("  python test_basic_ocr.py test_documents\\papers\\conference_paper.jpg")
    print("\nOr test all papers:")
    print("  Get-ChildItem test_documents\\papers\\*.jpg | ForEach-Object { python test_basic_ocr.py $_.FullName }")

if __name__ == "__main__":
    main()

