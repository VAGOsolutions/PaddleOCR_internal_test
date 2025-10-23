"""
Create sample test documents for PaddleOCR testing
Generates synthetic documents with tables, forms, and mixed content
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_simple_table():
    """Create a simple table document"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((300, 30), "Sales Report Q4 2024", fill='black', font=font_large)
    
    # Table headers
    y = 100
    headers = ["Product", "Q1", "Q2", "Q3", "Q4", "Total"]
    x_positions = [50, 200, 300, 400, 500, 650]
    
    # Draw header
    for i, header in enumerate(headers):
        draw.text((x_positions[i], y), header, fill='black', font=font_small)
    
    # Draw header line
    draw.line([(40, y+30), (750, y+30)], fill='black', width=2)
    
    # Table data
    data = [
        ["Laptop", "$45,000", "$52,000", "$48,000", "$61,000", "$206,000"],
        ["Tablet", "$28,000", "$31,000", "$29,000", "$35,000", "$123,000"],
        ["Phone", "$67,000", "$72,000", "$68,000", "$81,000", "$288,000"],
        ["Monitor", "$15,000", "$18,000", "$16,000", "$22,000", "$71,000"],
        ["Keyboard", "$8,000", "$9,000", "$8,500", "$11,000", "$36,500"]
    ]
    
    y += 50
    for row in data:
        for i, cell in enumerate(row):
            draw.text((x_positions[i], y), cell, fill='black', font=font_small)
        y += 40
    
    # Draw bottom line
    draw.line([(40, y), (750, y)], fill='black', width=2)
    
    # Total row
    y += 10
    draw.text((50, y), "Grand Total", fill='black', font=font_small)
    draw.text((650, y), "$724,500", fill='black', font=font_large)
    
    return img

def create_invoice_document():
    """Create a simple invoice document"""
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 32)
        font_large = ImageFont.truetype("arial.ttf", 20)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_title = font_large = font_small = ImageFont.load_default()
    
    # Title
    draw.text((300, 30), "INVOICE", fill='black', font=font_title)
    
    # Invoice details
    y = 100
    details = [
        "Invoice #: INV-2024-001",
        "Date: October 23, 2025",
        "Due Date: November 23, 2025",
        "",
        "Bill To:",
        "Acme Corporation",
        "123 Business Street",
        "New York, NY 10001",
        "",
        "From:",
        "Tech Solutions Inc.",
        "456 Tech Avenue",
        "San Francisco, CA 94105"
    ]
    
    for line in details:
        draw.text((50, y), line, fill='black', font=font_small)
        y += 35
    
    # Items table
    y += 20
    draw.line([(40, y), (760, y)], fill='black', width=2)
    y += 10
    
    # Headers
    draw.text((50, y), "Description", fill='black', font=font_large)
    draw.text((400, y), "Quantity", fill='black', font=font_large)
    draw.text((550, y), "Price", fill='black', font=font_large)
    draw.text((680, y), "Total", fill='black', font=font_large)
    
    y += 35
    draw.line([(40, y), (760, y)], fill='black', width=1)
    
    # Items
    items = [
        ("Software License", "10", "$500.00", "$5,000.00"),
        ("Technical Support", "12 months", "$200.00/mo", "$2,400.00"),
        ("Training Sessions", "5", "$300.00", "$1,500.00"),
        ("Installation Fee", "1", "$800.00", "$800.00")
    ]
    
    y += 10
    for item in items:
        draw.text((50, y), item[0], fill='black', font=font_small)
        draw.text((420, y), item[1], fill='black', font=font_small)
        draw.text((550, y), item[2], fill='black', font=font_small)
        draw.text((680, y), item[3], fill='black', font=font_small)
        y += 40
    
    # Total section
    y += 20
    draw.line([(500, y), (760, y)], fill='black', width=1)
    y += 15
    
    totals = [
        ("Subtotal:", "$9,700.00"),
        ("Tax (10%):", "$970.00"),
        ("Total Due:", "$10,670.00")
    ]
    
    for label, value in totals:
        draw.text((550, y), label, fill='black', font=font_large)
        draw.text((680, y), value, fill='black', font=font_large)
        y += 40
    
    # Footer
    y += 40
    draw.text((50, y), "Payment Terms: Net 30 days", fill='black', font=font_small)
    draw.text((50, y+30), "Thank you for your business!", fill='black', font=font_small)
    
    return img

def create_form_document():
    """Create a simple form document"""
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_label = ImageFont.truetype("arial.ttf", 16)
    except:
        font_title = font_label = ImageFont.load_default()
    
    # Title
    draw.text((250, 30), "Customer Registration Form", fill='black', font=font_title)
    
    # Form fields
    y = 100
    fields = [
        ("First Name:", "John"),
        ("Last Name:", "Doe"),
        ("Email:", "john.doe@email.com"),
        ("Phone:", "+1 (555) 123-4567"),
        ("Address:", "123 Main Street"),
        ("City:", "New York"),
        ("State:", "NY"),
        ("ZIP Code:", "10001"),
        ("Country:", "United States"),
        ("Company:", "Acme Corp"),
        ("Job Title:", "Software Engineer"),
        ("Department:", "Engineering")
    ]
    
    for label, value in fields:
        # Label
        draw.text((50, y), label, fill='black', font=font_label)
        # Line for input
        draw.line([(200, y+20), (750, y+20)], fill='gray', width=1)
        # Value
        draw.text((210, y), value, fill='blue', font=font_label)
        y += 60
    
    # Checkbox section
    y += 20
    draw.text((50, y), "Preferences:", fill='black', font=font_title)
    y += 40
    
    checkboxes = [
        "☑ Email notifications",
        "☐ SMS notifications",
        "☑ Newsletter subscription",
        "☐ Special offers"
    ]
    
    for checkbox in checkboxes:
        draw.text((70, y), checkbox, fill='black', font=font_label)
        y += 40
    
    # Signature
    y += 40
    draw.text((50, y), "Signature:", fill='black', font=font_label)
    draw.line([(200, y+20), (500, y+20)], fill='black', width=1)
    draw.text((550, y), "Date: 10/23/2025", fill='black', font=font_label)
    
    return img

def main():
    """Create all sample documents"""
    print("="*60)
    print("Creating Sample Test Documents")
    print("="*60)
    
    os.makedirs("test_documents/tables", exist_ok=True)
    os.makedirs("test_documents/invoices", exist_ok=True)
    os.makedirs("test_documents/forms", exist_ok=True)
    
    documents = [
        (create_simple_table, "test_documents/tables/sales_report.jpg", "Sales Report Table"),
        (create_invoice_document, "test_documents/invoices/sample_invoice.jpg", "Sample Invoice"),
        (create_form_document, "test_documents/forms/registration_form.jpg", "Registration Form")
    ]
    
    print("\nCreating documents...")
    for create_func, filepath, description in documents:
        try:
            img = create_func()
            img.save(filepath, quality=95)
            print(f"✓ Created: {description} -> {filepath}")
        except Exception as e:
            print(f"✗ Failed to create {description}: {e}")
    
    print("\n" + "="*60)
    print("Sample documents created successfully!")
    print("="*60)
    print("\nTest these documents with:")
    print("  python test_document_parsing.py test_documents/tables/sales_report.jpg --table")
    print("  python test_document_parsing.py test_documents/invoices/sample_invoice.jpg")
    print("  python test_document_parsing.py test_documents/forms/registration_form.jpg")

if __name__ == "__main__":
    main()

