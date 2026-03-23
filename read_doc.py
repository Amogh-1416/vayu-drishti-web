import docx

def read_document(filepath):
    try:
        doc = docx.Document(filepath)
        print(f"Successfully opened {filepath}")
        print("--- EXTRACTED TEXT ---")
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                print(text)
        print("--- END EXTRACTED TEXT ---")
    except Exception as e:
        print(f"Error reading document: {e}")

if __name__ == "__main__":
    read_document('Vayu-Drishti.docx')
