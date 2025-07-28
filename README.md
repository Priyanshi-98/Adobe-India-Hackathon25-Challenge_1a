# Adobe-India-Hackathon25-Challenge_1a

## Overview
This is my submission for Round 1A: Understand Your Document of the Adobe India Hackathon 2025 under the “Connecting the Dots” theme.
The goal of this challenge is to extract a clean, structured outline from a PDF — including the Title, and Headings (H1, H2, H3) — and output the result as a standardized JSON. This is intended to enable smarter document interaction, powering applications like semantic search, navigation, and AI-based summarization.
<br><br>

## Approach Used:
This solution uses a rule-based pipeline to ensure lightweight, deterministic, and fast execution under all hardware constraints.
### Key Steps:
- Text Extraction with Layout Info:
    - Using pdfplumber, we extract each word’s font size, font name, and bounding box (x0, x1, top, bottom) along with text content from every page.
- Line Reconstruction:
    - Words are grouped into lines using the top coordinate, and then merged based on spatial gaps (x0/x1) to form full sentences.
- Heading Detection:
    - Font sizes are clustered to detect "heading levels".
    - The most common font size is assumed to be the body text.
    - Font sizes larger than body size are mapped to H1, H2, and H3 based on descending order.
- Filtering & Heuristics:
    - Headings are filtered based on:
      - Appearance near center of the page
      - Avoiding lines with excessive dots, symbols, or duplicates
      - Excluding the title from heading list
      - Avoiding misclassified form-like content
- Title Extraction:
    - The largest font text on page 0, located near the top, is selected as the document title.
- JSON Output Generation:
    - The final output is a JSON matching the required schema.
<br><br>

## Output JSON Format
```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 0 },
    { "level": "H2", "text": "What is AI?", "page": 1 },
    { "level": "H3", "text": "History of AI", "page": 2 }
  ]
}
```
<br><br>

## Directory Structure
├── process_pdfs.py  
├── requirements.txt  <br>
├── Dockerfile            <br>
├── README.md             <br>
├── /input                <br>
└── /output               <br>
<br>

## Build and Run Instructions
Build Docker Image
docker build --platform linux/amd64 -t pdf-processor .

Run with Mounted Volumes
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-processor
<br><br>

## Libraries Used
- pdfplumber: for detailed PDF text + layout extraction
- Python standard libraries: collections, json, os, pathlib
<br><br>

## Testing Strategy
This code has been tested across:
- Short PDFs with only headings
- Long PDFs (10+ pages) with mixed formatting
- PDFs with center-aligned vs left-aligned headings
- Edge cases like numbered lists or short forms
<br><br>

## Possible Improvements
- Integrate ML/LLM models for semantic-aware heading detection
- Enhance heading-level classification using clustering + layout patterns
- Add support for visual cues like bold, caps-lock, or indentation
