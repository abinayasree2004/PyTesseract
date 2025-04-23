import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
import os
import json
from datetime import datetime

def process_invoice_pdf(pdf_path, base_output_folder="Outputs", dpi=300):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename_base = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(base_output_folder, f"{filename_base}_{timestamp}")
    os.makedirs(output_folder, exist_ok=True)

    print("[INFO] Converting PDF to images...")
    pages = convert_from_path(pdf_path, dpi=dpi)

    wordlist = []  # Final output list of lists

    for page_num, page in enumerate(pages):
        img = np.array(page)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

        page_words = []  # Words for this page

        for i in range(len(ocr_data['text'])):
            word = ocr_data['text'][i].strip()
            if word != "":
                x, y, w, h = (
                    ocr_data['left'][i],
                    ocr_data['top'][i],
                    ocr_data['width'][i],
                    ocr_data['height'][i]
                )
                x1, y1 = x, y
                x2, y2 = x + w, y + h

                page_words.append({
                    "value": word,
                    "bboxes": [[x1, y1], [x2, y2]]
                })

                # Draw boxes
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, word, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        wordlist.append(page_words)

        # Save image with boxes
        image_out_path = os.path.join(output_folder, f"{filename_base}_page_{page_num + 1}_{timestamp}.png")
        cv2.imwrite(image_out_path, img)
        print(f"[INFO] Image saved: {image_out_path}")

    # Save JSON with Python-style variable assignment
    json_out_path = os.path.join(output_folder, f"{filename_base}_wordlist_{timestamp}.json")
    with open(json_out_path, "w", encoding="utf-8") as f:
        f.write("wordlist = ")
        json.dump(wordlist, f, indent=4)

    print(f"[INFO] JSON saved to: {json_out_path}")

# Example usage
if __name__ == "__main__":
    pdf_file = input("Enter the name of the PDF file to scan: ")
    process_invoice_pdf(pdf_file)
