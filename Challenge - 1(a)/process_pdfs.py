# FINAL process_pdfs.py SCRIPT (for Docker)
import fitz
import json
import os
import re
import pandas as pd
import joblib
from collections import defaultdict

# --- Configuration ---
INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

# --- Load the Trained Model ---
# This happens once when the script starts.
try:
    MODEL = joblib.load('document_outline_model.pkl')
    print("ML Model loaded successfully.")
except FileNotFoundError:
    print("FATAL ERROR: 'document_outline_model.pkl' not found. Make sure it's in the same directory.")
    MODEL = None

# --- Feature Extraction and Line Reconstruction (must match training) ---
def reconstruct_lines_from_page(page):
    spans = [span for block in page.get_text("dict")["blocks"] if block['type'] == 0 for line in block['lines'] for span in line['spans']]
    if not spans: return []
    lines_by_baseline = defaultdict(list)
    for span in spans:
        lines_by_baseline[round(span['bbox'][1])].append(span)
    reconstructed = []
    for baseline in sorted(lines_by_baseline.keys()):
        line_spans = sorted(lines_by_baseline[baseline], key=lambda s: s['bbox'][0])
        full_text = " ".join(s['text'].strip() for s in line_spans).strip()
        if full_text:
            rep_span = line_spans[0]
            reconstructed.append({"text": full_text, "size": rep_span['size'], "flags": rep_span['flags'], "y_pos": baseline})
    return reconstructed

def extract_features_for_prediction(lines, body_size):
    """Extracts features for a list of lines, ready for prediction."""
    features_list = []
    for line in lines:
        text = line['text']
        features = {
            'font_size': round(line['size']), 'size_vs_body': round(line['size']) - body_size,
            'is_bold': 1 if line['flags'] & (1 << 4) else 0, 'y_pos': line['y_pos'],
            'line_length': len(text), 'word_count': len(text.split()),
            'is_all_caps': 1 if text.isupper() and len(text) > 1 else 0,
            'starts_with_number': 1 if re.match(r'^\s*(\d+(\.\d+)*)\s+', text) else 0,
            'ends_with_colon': 1 if text.strip().endswith(':') else 0,
        }
        features_list.append(features)
    return pd.DataFrame(features_list)

def find_title(page):
    lines = reconstruct_lines_from_page(page)
    if not lines: return "Untitled Document"
    max_size = max(line['size'] for line in lines)
    title_parts = [line['text'] for line in lines if line['size'] >= max_size - 1]
    return " ".join(title_parts)

def process_pdf_with_ml(pdf_path):
    if not MODEL: return None
    doc = fitz.open(pdf_path)
    if len(doc) == 0: return {"title": "Empty Document", "outline": []}

    title = find_title(doc[0])
    
    # Get body size for feature engineering
    sizes = [round(span['size']) for page in doc for block in page.get_text("dict")['blocks'] if block['type']==0 for line in block['lines'] for span in line['spans']]
    body_size = pd.Series(sizes).mode()[0] if sizes else 10

    outline = []
    for page_num, page in enumerate(doc):
        lines = reconstruct_lines_from_page(page)
        if not lines: continue

        # Predict labels for all lines on the page at once (much faster)
        features_df = extract_features_for_prediction(lines, body_size)
        predictions = MODEL.predict(features_df)

        for i, line in enumerate(lines):
            label = predictions[i]
            if label != 'Body':
                 # Filter out title text from the outline
                if page_num == 0 and line['text'] in title:
                    continue
                outline.append({"level": label, "text": line['text'], "page": page_num + 1})
    
    doc.close()
    return {"title": title, "outline": outline}

def main():
    print(">>> RUNNING FINAL ML-DRIVEN ENGINE <<<")
    if not os.path.exists(INPUT_DIR): os.makedirs(INPUT_DIR, exist_ok=True)
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing {filename} with ML model...")
            structured_data = process_pdf_with_ml(pdf_path)
            if structured_data:
                json_filename = os.path.splitext(filename)[0] + ".json"
                output_path = os.path.join(OUTPUT_DIR, json_filename)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(structured_data, f, indent=4, ensure_ascii=False)
                print(f"  -> Successfully created {json_filename}")
    print("Processing finished.")

if __name__ == "__main__":
    main()