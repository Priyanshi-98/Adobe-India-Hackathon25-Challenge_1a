# Adobe-India-Hackathon25-Challenge_1a

## Overview

This is my submission for **Round 1A: Understand Your Document** of the **Adobe India Hackathon 2025** under the “Connecting the Dots” theme.

The goal of this challenge is to extract a clean, structured outline from a PDF — including the **Title**, and **Headings (H1, H2, H3)** — and output the result as a standardized JSON. This enables smarter document interaction, powering applications like semantic search, contextual navigation, and AI-based summarization.

---

## Vision

In today’s world of **information overload**, it's common to work with dozens of PDFs, research papers, and project documents. The vision of this challenge—and this submission—is to go beyond viewing documents in isolation.

We aim to:

-  **Automate the discovery of relevant information** across a user’s library
-  **Surface insights from older documents** while reading new ones, reducing repetitive manual searching
-  **Connect ideas, sections, and contradictions across multiple PDFs**
-  **Understand** the document—not just view it
-  Lay the foundation for intelligent document experiences through modular challenges:
    - **1A:** Identify structure (Title, H1/H2/H3)
    - **1B:** Relate and rank relevant sections across documents for a specific user persona
- **Finally** Seamlessly surface knowledge from previous reads into new reading sessions

By focusing on accurate outline extraction in 1A, we build the groundwork to enable deeper inter-document connections in future rounds.

---

## Approach & Context

This solution uses a **rule-based pipeline** to ensure lightweight, deterministic, and fast execution under all hardware constraints.

### Key Steps:

#### Text Extraction with Layout Info
- Using `pdfplumber`, we extract each word’s:
  - Font size
  - Font name
  - Bounding box (`x0`, `x1`, `top`, `bottom`)
  - Text content

#### Line Reconstruction
- Words are grouped into lines using `top` alignment
- Lines are reassembled by measuring gaps between adjacent words

#### Heading Detection
- Font sizes are clustered to detect heading levels
- The most common font size is considered body text
- Larger font sizes are mapped to H1, H2, and H3 in descending order

#### Filtering & Heuristics
- Headings are filtered based on:
  - Center alignment (to avoid body text)
  - Avoiding dotted lines and symbols
  - Eliminating duplicates and title repetitions
  - Excluding form-like content heuristically

#### Title Extraction
- The largest font text on page 0 is considered the document title

#### JSON Output Generation
- Final output is a JSON with title and outline in required schema

---

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

---

## Directory Structure
├── process_pdfs.py  
├── requirements.txt  <br>
├── Dockerfile            <br>
├── README.md             <br>
├── /input                <br>
└── /output               <br>
<br>

---

## Build and Run Instructions
- Build Docker Image
    - docker build --platform linux/amd64 -t pdf-processor .

- Run with Mounted Volumes
    - docker run --rm -v "${PWD}/input:/app/input" -v "${PWD}/output:/app/output" --network none pdf-processor
<br><br>

---

## Libraries Used
- pdfplumber: for detailed PDF text + layout extraction
- Python standard libraries: collections, json, os, pathlib
<br><br>

---

## Testing Strategy
This code has been tested across:
- Short PDFs with only headings
- Long PDFs (10+ pages) with mixed formatting
- PDFs with center-aligned vs left-aligned headings
- Edge cases like numbered lists or short forms
<br><br>

---

## Possible Improvements
- Integrate ML/LLM models for semantic-aware heading detection
- Enhance heading-level classification using clustering + layout patterns
- Add support for visual cues like bold, caps-lock, or indentation
