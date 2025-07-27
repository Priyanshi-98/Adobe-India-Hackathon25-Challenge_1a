import os
import json
import pdfplumber
from pathlib import Path
from collections import defaultdict, Counter

def merge_line_words(line_words):
    line_words = sorted(line_words, key=lambda w: w['x0'])
    merged = line_words[0]['text']
    prev_x1 = line_words[0]['x1']

    for word in line_words[1:]:
        space_gap = word['x0'] - prev_x1
        if space_gap > 1.5:
            merged += " "
        merged += word['text']
        prev_x1 = word['x1']

    return merged

def extract_text_blocks(pdf):
    blocks = []
    for i, page in enumerate(pdf.pages):
        words = page.extract_words(extra_attrs=["size", "fontname", "x0", "x1", "top", "bottom"])
        lines = defaultdict(list)

        for word in words:
            line_key = round(word['top'], 1)
            lines[line_key].append(word)

        for line_words in lines.values():
            line_words = sorted(line_words, key=lambda w: w['x0'])
            line_text = merge_line_words(line_words)
            avg_size = sum(word['size'] for word in line_words) / len(line_words)
            font = line_words[0]['fontname']
            blocks.append({
                "text": line_text.strip(),
                "size": round(avg_size, 1),
                "fontname": font,
                "page": i,
                "x0": line_words[0]['x0'],
                "x1": line_words[-1]['x1']
            })

    return blocks

def cluster_font_sizes(text_blocks):
    sizes = [round(block['size'], 1) for block in text_blocks]
    size_counts = Counter(sizes)
    if not size_counts:
        return {}
    most_common_size, _ = size_counts.most_common(1)[0]
    candidate_sizes = [s for s in sorted(size_counts.keys(), reverse=True) if s > most_common_size]
    level_map = {}
    level_names = ["H1", "H2", "H3"]
    for i, size in enumerate(candidate_sizes):
        if i >= len(level_names):
            break
        level_map[size] = level_names[i]
    return level_map

def extract_title(blocks):
    page0 = [b for b in blocks if b["page"] == 0]
    if not page0:
        return ""
    max_size = max(b['size'] for b in page0)
    top_blocks = [b for b in page0 if b['size'] == max_size]
    lines = defaultdict(list)
    for b in top_blocks:
        line_key = round(b.get("top", 0), 1)
        lines[line_key].append(b)
    top_line = sorted(lines.items(), key=lambda item: item[0])[0][1]
    top_line = sorted(top_line, key=lambda b: b['x0'])
    return "  ".join(b['text'] for b in top_line).strip()

def is_probably_form_document(blocks):
    font_sizes = [b["size"] for b in blocks]
    if len(set(b["page"] for b in blocks)) > 1:
        return False
    avg_size = sum(font_sizes) / len(font_sizes)
    unique_fonts = set(font_sizes)
    has_numbered_lines = any(
        b["text"].strip().startswith(tuple(str(i) for i in range(1, 15)))
        for b in blocks
    )
    return avg_size < 11 and len(unique_fonts) <= 3 and not has_numbered_lines

def extract_outline(blocks):
    level_map = cluster_font_sizes(blocks)
    outline = []
    seen = set()
    form_mode = is_probably_form_document(blocks)
    title_text = extract_title(blocks)

    for block in blocks:
        text = block['text'].strip()
        size = block['size']
        level = level_map.get(size)

        if text.count(".") > 5:
            continue
        if not level:
            continue
        text_center = (block['x0'] + block['x1']) / 2
        if not (200 <= text_center <= 400):
            continue
        if form_mode:
            continue
        if text == title_text:
            continue
        if text not in seen:
            seen.add(text)
            outline.append({
                "level": level,
                "text": text,
                "page": block['page']
            })
    return outline

def process_pdf(path):
    with pdfplumber.open(path) as pdf:
        blocks = extract_text_blocks(pdf)
        title = extract_title(blocks)
        outline = extract_outline(blocks)
        return {
            "title": title,
            "outline": outline
        }

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*.pdf"))

    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name}...")
        result = process_pdf(pdf_file)
        output_file = output_dir / f"{pdf_file.stem}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"{pdf_file.name} processed -> {output_file.name}")

if __name__ == "__main__":
    print("Starting processing pdfs")
    process_pdfs()
    print("Completed processing pdfs")
