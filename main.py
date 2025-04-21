import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import os
from datetime import datetime

def process_invoice_pdf(pdf_path, base_output_folder="Outputs", dpi=300):
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a unique folder inside Outputs
    filename_base = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(base_output_folder, f"{filename_base}_{timestamp}")
    os.makedirs(output_folder, exist_ok=True)

    print("[INFO] Converting PDF to images...")
    pages = convert_from_path(pdf_path, dpi=dpi)

    full_text = ""

    for page_num, page in enumerate(pages):
        # Convert PIL image to OpenCV format
        img = np.array(page)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # OCR with bounding box data
        ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        page_text = pytesseract.image_to_string(img)

        # Append clean text from this page
        full_text += f"\n--- Page {page_num + 1} ---\n{page_text.strip()}\n"

        # Draw boxes around detected words
        for i in range(len(ocr_data['text'])):
            word = ocr_data['text'][i]
            if word.strip() != "":
                x, y, w, h = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, word, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        # Save the image with boxes
        image_out_path = os.path.join(output_folder, f"{filename_base}_page_{page_num + 1}_{timestamp}.png")
        cv2.imwrite(image_out_path, img)
        print(f"[INFO] Image saved: {image_out_path}")

    # Save the clean extracted text
    text_out_path = os.path.join(output_folder, f"{filename_base}_text_output_{timestamp}.txt")
    with open(text_out_path, "w", encoding="utf-8") as f:
        f.write(full_text.strip())

    print(f"[INFO] Text saved to: {text_out_path}")

# Example usage
if __name__ == "__main__":
    pdf_file = input("Enter the name of the PDF file to scan: ")
    process_invoice_pdf(pdf_file)