# PyTesseract
Invoice OCR Scanner with Bounding Boxes
---------------------------------------

This Python project uses pytesseract, pdf2image, and OpenCV to process PDF invoices, extract text using OCR, draw bounding boxes around detected words, and save both annotated images and plain text files.

Features:
- Convert invoice PDFs into high-res images
- Extract text using Tesseract OCR
- Draw bounding boxes around detected text
- Save clean .txt files with the extracted content
- Save annotated images for visual verification

Requirements:
- Python 3.7+
- Tesseract-OCR
- Poppler

Install required Python packages:
pip install pytesseract pdf2image opencv-python Pillow numpy

Setup:
1. Install Tesseract (Windows):
   https://github.com/UB-Mannheim/tesseract/wiki
   Add this to your script:
   pytesseract.pytesseract.tesseract_cmd = r'C:\path\to\Tesseract-OCR\tesseract.exe'

2. Install Poppler (Windows):
   https://github.com/oschwartz10612/poppler-windows
   Add Poppler's bin folder to the script:
   os.environ["PATH"] += os.pathsep + r'C:\path\to\poppler\bin'

How to Use:
1. Place your PDF invoice in the folder (e.g., invoice.pdf)
2. Run the script:
   python main.py
3. Outputs will be in 'output_invoice/' as:
   - Extracted text: page_1.txt, etc.
   - Annotated images: page_1.jpg, etc.

Folder Structure:
output_invoice/...
