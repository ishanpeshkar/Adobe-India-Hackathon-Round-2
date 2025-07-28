# Connecting the Dots Challenge - Round 1A: Document Outline Extractor

This project is a solution for Round 1A of the "Connecting the Dots" hackathon. It provides a containerized application that automatically extracts a structured outline (Title, H1, H2, H3) from PDF files.

## Approach

The core of this solution is a heuristic-based system that analyzes PDF content to identify headings without relying on a single attribute like font size. This makes it robust against variations in PDF formatting. The process works as follows:

1.  **Style Analysis**: The script first performs a quick analysis of the initial pages of the PDF to build a profile of the document's font styles. It identifies the most common font size, which is assumed to be the body text.

2.  **Heading Identification**: Any text that is both **bolder** and **larger** than the determined body text is considered a potential heading. This two-factor check significantly improves accuracy.

3.  **Hierarchical Classification**: The identified heading styles are grouped by font size. The group with the largest font size is classified as `H1`, the second largest as `H2`, and the third as `H3`. This creates a clear and logical hierarchy.

4.  **Content Extraction**: The script iterates through every page, extracting text lines that match the pre-identified heading styles. Additional filters are applied to discard irrelevant text (e.g., headers/footers, very short lines).

5.  **Title Detection**: The title of the document is assumed to be the first `H1` heading encountered. If no `H1` is found, it defaults to the first heading in the outline.

This entire process is designed to be fast, offline, and self-contained within the Docker image.

## Libraries Used

*   **PyMuPDF (`fitz`)**: Chosen for its high performance, low memory footprint, and rich text extraction capabilities. It allows access to detailed font information (size, weight, color) and positional data, which is essential for the heuristic model.

## How to Build and Run the Solution

The solution is packaged in a Docker container for easy and consistent execution.

### Prerequisites

*   Docker installed and running.

### Build the Docker Image

Navigate to the project's root directory (where the `Dockerfile` is located) and run the following command. This will build the image with the name `outline-extractor`.

```bash
docker build --platform linux/amd64 -t outline-extractor .
```

### Run the Solution

Once the image is built, you can run it to process your PDFs.

1.  Place your input PDF files into a directory named `input` in your current location.
2.  Create an empty directory named `output` where the JSON results will be saved.
3.  Execute the following Docker command:

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  outline-extractor
```

**Explanation of the command:**

*   `docker run --rm`: Runs the container and automatically removes it when it finishes.
*   `-v $(pwd)/input:/app/input`: Mounts your local `input` directory to the `/app/input` directory inside the container.
*   `-v $(pwd)/output:/app/output`: Mounts your local `output` directory to the `/app/output` directory, where the script will write the JSON files.
*   `--network none`: Ensures the container runs without any network access, as per the challenge constraints.
*   `outline-extractor`: The name of the image to run.

The container will automatically process every `.pdf` file in the `input` directory and generate a corresponding `.json` file in the `output` directory.