import docx

def evaluate_doc(filepath):
    doc = docx.Document(filepath)
    print(f"--- Document Content for {filepath} ---")

    figures = []
    content = ""

    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        content += text + " "
        if text.startswith("Fig.") or "Figure" in text or "Fig " in text:
            figures.append((i, text))

    print("\n--- Found Potential Figure Placeholders ---")
    for idx, f in figures:
        print(f"Para {idx}: {f}")

    print("\n--- Keyword Analysis ---")
    keywords = ["YOLO", "RescueNet", "A*", "Routing", "Grid", "Django", "CesiumJS", "WebSocket", "Redis", "Heridal", "PostGIS"]
    for kw in keywords:
        found = content.lower().count(kw.lower())
        print(f"{kw}: {found} occurrences")

if __name__ == '__main__':
    evaluate_doc('Vayu-Drishti-IEEE (1).docx')
