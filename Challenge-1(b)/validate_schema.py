#!/usr/bin/env python3
"""
Schema validation script for Challenge 1B output
Adobe India Hackathon 2025
"""

import json
import sys
from pathlib import Path
import jsonschema
from typing import List

def color_text(message, text_color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    return f"{colors.get(text_color, '')}{message}{colors['reset']}"

def get_schema_path() -> Path:
    return Path(__file__).parent / "challenge1b_output_schema.json"

def read_json_file(file_location: Path) -> dict:
    with open(file_location, 'r', encoding='utf-8') as file_handle:
        return json.load(file_handle)

def print_schema_load_error(error, schema_location):
    print(color_text(f"Schema file error: {error} ({schema_location})", "red"))
    sys.exit(1)

def load_schema() -> dict:
    schema_location = get_schema_path()
    try:
        return read_json_file(schema_location)
    except FileNotFoundError as error:
        print_schema_load_error("not found", schema_location)
    except json.JSONDecodeError as error:
        print_schema_load_error(f"invalid JSON: {error}", schema_location)

def check_sections_and_subsections(data_output: dict):
    section_data = data_output.get('extracted_sections', [])
    subsection_data = data_output.get('subsection_analysis', [])
    if not section_data and not subsection_data:
        print(color_text("  Warning: No sections or subsections found", "yellow"))

def check_importance_ranks(section_list):
    rank_values = [s.get('importance_rank', 0) for s in section_list]
    if rank_values and rank_values != sorted(rank_values):
        print(color_text("  Warning: Importance ranks are not sequential", "yellow"))

def semantic_checks(data_output: dict):
    check_sections_and_subsections(data_output)
    section_data = data_output.get('extracted_sections', [])
    if section_data:
        check_importance_ranks(section_data)

def validate_json_schema(output_data: dict, schema: dict):
    try:
        jsonschema.validate(instance=output_data, schema=schema)
        return True, ""
    except jsonschema.ValidationError as e:
        return False, f"{e.message}\n      Path: {' -> '.join(str(p) for p in e.path)}"

def validate_output_file(file_path: Path, schema: dict) -> bool:
    try:
        output_data = read_json_file(file_path)
    except FileNotFoundError:
        print(color_text(f"  File not found: {file_path}", "red"))
        return False
    except json.JSONDecodeError as e:
        print(color_text(f"  Invalid JSON: {e}", "red"))
        return False

    valid, error_msg = validate_json_schema(output_data, schema)
    if not valid:
        print(color_text(f"  Schema validation error: {error_msg}", "red"))
        return False

    semantic_checks(output_data)
    print(color_text("  Valid JSON structure", "green"))
    print(color_text("  Perfect compliance!", "blue"))
    return True

def get_output_patterns() -> List[str]:
    return [
        "challenge1b_output*.json",
        "*output*.json",
        "round_1b*.json"
    ]

def find_output_files(directory: Path) -> List[Path]:
    files = []
    for pattern in get_output_patterns():
        files.extend(directory.glob(pattern))
    return sorted(set(files))

def print_summary(valid_files, total_files):
    print("\n" + "=" * 40)
    print(color_text("Validation Summary:", "blue"))
    print(f"   Valid files: {color_text(f'{valid_files}/{total_files}', 'green' if valid_files == total_files else 'yellow')}")
    if valid_files == total_files:
        print(color_text("   All files passed validation!", "green"))
    else:
        print(color_text(f"   {total_files - valid_files} file(s) failed validation", "yellow"))

def get_files_to_validate(argv, output_dir: Path) -> List[Path]:
    if len(argv) > 1:
        return [Path(arg) for arg in argv[1:]]
    return find_output_files(output_dir)

def main():
    print(color_text("Challenge 1B Output Validator", "blue"))
    print("=" * 40)
    schema = load_schema()
    print(color_text("Schema loaded successfully", "green"))

    output_dir = Path(__file__).parent / "output"
    files_to_validate = get_files_to_validate(sys.argv, output_dir)

    if not files_to_validate:
        print(color_text("No output files found to validate", "red"))
        return 1

    print(color_text(f"Found {len(files_to_validate)} output file(s)", "blue"))
    valid_files = 0
    total_files = len(files_to_validate)

    for file_path in files_to_validate:
        print(f"\n{color_text('Validating:', 'blue')} {file_path.name}")
        if validate_output_file(file_path, schema):
            valid_files += 1

    print_summary(valid_files, total_files)
    return 0 if valid_files == total_files else 1

if __name__ == "__main__":
    sys.exit(main())
