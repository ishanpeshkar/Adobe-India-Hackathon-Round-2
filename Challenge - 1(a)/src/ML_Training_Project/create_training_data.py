import fitz  # PyMuPDF
import os
import pandas as pd
from collections import defaultdict
import re

def reconstruct_lines_from_page(page):
    """Manually reconstructs lines from text spans based on vertical position."""
    spans = [span for block in page.get_text("dict")["blocks"] if block['type'] == 0 for line in block['lines'] for span in line['spans']]
    if not spans: return []

    lines_by_baseline = defaultdict(list)
    for span in spans:
        baseline = round(span['bbox'][1])
        lines_by_baseline[baseline].append(span)

    reconstructed_lines = []
    for baseline in sorted(lines_by_baseline.keys()):
        line_spans = sorted(lines_by_baseline[baseline], key=lambda s: s['bbox'][0])
        full_text = " ".join(span['text'].strip() for span in line_spans).strip()
        if not full_text: continue
        
        rep_span = line_spans[0]
        reconstructed_lines.append({
            "text": full_text, "size": rep_span['size'], "font": rep_span['font'], 
            "flags": rep_span['flags'], "y_pos": baseline
        })
    return reconstructed_lines

def extract_features(doc_path):
    """Extracts a feature vector for every line in a document."""
    doc = fitz.open(doc_path)
    all_features = []
    
    # Analyze document for body size
    sizes = [round(span['size']) for page in doc for block in page.get_text("dict")['blocks'] if block['type']==0 for line in block['lines'] for span in line['spans']]
    body_size = pd.Series(sizes).mode()[0] if sizes else 10

    for page_num, page in enumerate(doc):
        lines = reconstruct_lines_from_page(page)
        for line in lines:
            text = line['text']
            
            features = {
                'text': text,
                'font_size': round(line['size']),
                'size_vs_body': round(line['size']) - body_size,
                'is_bold': 1 if line['flags'] & (1 << 4) else 0,
                'y_pos': line['y_pos'],
                'line_length': len(text),
                'word_count': len(text.split()),
                'is_all_caps': 1 if text.isupper() and len(text) > 1 else 0,
                'starts_with_number': 1 if re.match(r'^\s*(\d+(\.\d+)*)\s+', text) else 0,
                'ends_with_colon': 1 if text.strip().endswith(':') else 0,
                'page_num': page_num,
                'doc_name': os.path.basename(doc_path),
                'label': '' # This is what we will fill in manually
            }
            all_features.append(features)
    doc.close()
    return all_features

def main():
    input_dir = 'input'
    all_lines_data = []
    print("Starting feature extraction...")
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            print(f"  Processing {filename}...")
            pdf_path = os.path.join(input_dir, filename)
            all_lines_data.extend(extract_features(pdf_path))
    
    df = pd.DataFrame(all_lines_data)
    output_path = 'features.csv'
    df.to_csv(output_path, index=False)
    print(f"\nFeature extraction complete! Saved to {output_path}")
    print("Next Step: Open 'features.csv' in a spreadsheet editor and fill in the 'label' column.")

if __name__ == "__main__":
    main()