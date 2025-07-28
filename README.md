# 📚✨ PDF Insight Extractor - Connecting the Dots Challenge ✨📚

<div align="center">
  
![Header Banner](https://placehold.co/1200x400/2d2d4a/white?text=PDF+Insight+Extractor) <!-- Replace with actual banner image -->
  
[![Docker Build](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python Version](https://img.shields.io/badge/Python-3.10+-yellow?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

## 🌟 Project Overview

Welcome to **PDF Insight Extractor**, our innovative solution for the *"Connecting the Dots"* hackathon challenge! This tool transforms static PDFs into intelligent, structured documents by:

- 🔍 **Automatically extracting** titles and hierarchical headings (H1-H3)
- 🧠 **Understanding document structure** like a human would
- 🚀 **Delivering JSON output** ready for interactive applications

Built with cutting-edge techniques and packaged for seamless deployment, our solution bridges the gap between documents and machine understanding.

## 🏆 Challenge Context

> *"What if every time you opened a PDF, it didn't just sit there—it spoke to you, connected ideas, and narrated meaning across your entire library?"*

Our mission: **Reimagine PDFs as intelligent, interactive experiences** that understand structure and surface insights.

```mermaid
graph TD
    A[Raw PDF] --> B(Structure Detection)
    B --> C{Heading Analysis}
    C --> D[H1 Titles]
    C --> E[H2 Sections]
    C --> F[H3 Subsections]
    D --> G[Structured JSON]
    E --> G
    F --> G
    G --> H[Interactive Applications] ```



# 🛠 Technical Approach

## 🔬 Hybrid Analysis Engine

We combine **machine learning insights** with **heuristic rules** for robust performance:

### Visual Feature Extraction
- Font size, weight, and style analysis
- Positional context understanding
- Statistical distribution modeling

### Hierarchical Classification
- Multi-level heading identification
- Context-aware title detection
- Adaptive thresholding for diverse documents

### Output Generation
- Clean JSON serialization
- Page number mapping
- Validation and error handling

## 📚 Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| PDF Parsing | PyMuPDF (fitz) | High-performance text extraction |
| ML Framework | scikit-learn | Heading classification |
| Feature Engine | Custom Python | Contextual analysis |
| Containerization | Docker | Reproducible execution |

## 🚀 Getting Started

### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- AMD64 architecture system

### Installation & Usage

```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-insight-extractor .

# Prepare your PDFs
mkdir -p input output
cp your_document.pdf input/

# Run the extractor
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-insight-extractor

# Retrieve results
# Check the output/ directory for JSON files
# Each input PDF will have a corresponding .json output
