import json
import os
from utils.parser import extract_text_from_pdf

def load_json_config(config_file_path):
    """Load JSON configuration from a file."""
    with open(config_file_path, "r", encoding="utf-8") as file_handle:
        return json.load(file_handle)

def colored_terminal_text(display_text, color_code_value):
    """Return colored text for terminal output."""
    return f"\033[{color_code_value}m{display_text}\033[0m"

def get_pdf_file_path(base_directory, file_name):
    """Construct the full path to a PDF file."""
    return os.path.join(base_directory, "PDFs", file_name)

def extract_sample_pages(file_path, page_count=3):
    """Extract text from the first few pages of a PDF."""
    page_data = extract_text_from_pdf(file_path)
    return page_data[:page_count]

def append_metadata(meta_info, doc_filename):
    """Append document name to metadata."""
    meta_info["input_documents"].append(doc_filename)

def add_extracted_section(sections_list, document_name, section_heading, rank_value, page_number):
    """Add extracted section details."""
    sections_list.append({
        "document": document_name,
        "section_title": section_heading,
        "importance_rank": rank_value,
        "page_number": page_number
    })

def add_subsection_analysis(analysis_list, document_name, content_text, page_number):
    """Add subsection analysis details."""
    analysis_list.append({
        "document": document_name,
        "refined_text": content_text[:300],
        "page_number": page_number
    })

def process_single_document(doc_config, base_directory, output_dict):
    """Process a single document and update output data."""
    pdf_filename = doc_config["filename"]
    section_title = doc_config["title"]
    pdf_filepath = get_pdf_file_path(base_directory, pdf_filename)

    if not os.path.exists(pdf_filepath):
        print(colored_terminal_text(f"File not found: {pdf_filepath}", "31"))
        return

    sample_page_data = extract_sample_pages(pdf_filepath)
    append_metadata(output_dict["metadata"], pdf_filename)

    for idx, page_info in enumerate(sample_page_data):
        add_extracted_section(
            output_dict["extracted_sections"],
            pdf_filename,
            section_title,
            idx + 1,
            page_info["page_number"]
        )
        add_subsection_analysis(
            output_dict["subsection_analysis"],
            pdf_filename,
            page_info["text"],
            page_info["page_number"]
        )

def process_collection_documents(configuration_data, collection_directory):
    """Process all documents in a collection."""
    output_json_file_path = os.path.join(collection_directory, "challenge1b_output.json")
    output_data_structure = {
        "metadata": {
            "input_documents": [],
            "persona": configuration_data["persona"]["role"],
            "job_to_be_done": configuration_data["job_to_be_done"]["task"]
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for document_item in configuration_data["documents"]:
        process_single_document(document_item, collection_directory, output_data_structure)

    with open(output_json_file_path, "w", encoding="utf-8") as output_file:
        json.dump(output_data_structure, output_file, indent=2)

    print(colored_terminal_text(f"Output written to {output_json_file_path}", "32"))

def process_all_collections(collection_names):
    """Process all collections listed."""
    for collection_name in collection_names:
        input_json_path = os.path.join(collection_name, "challenge1b_input.json")
        if os.path.exists(input_json_path):
            print(colored_terminal_text(f"\nProcessing {collection_name}", "34"))
            config = load_json_config(input_json_path)
            process_collection_documents(config, collection_name)
        else:
            print(colored_terminal_text(f"Skipping {collection_name}: No input JSON found.", "33"))

def main():
    collections = ["Collection 1", "Collection 2", "Collection 3"]
    process_all_collections(collections)

if __name__ == "__main__":
    main()