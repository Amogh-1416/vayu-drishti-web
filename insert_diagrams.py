import docx
from docx.shared import Inches, Pt
import os

def insert_diagrams(filepath, output_path):
    doc = docx.Document(filepath)

    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()

        # Look for placeholders like "Fig.1:", "Fig. 2:", etc. in the original text
        if "Fig.1 :" in text or "Fig.1:" in text:
            p.text = "" # Clear placeholder text
            if os.path.exists('paper_assets/arch.png'):
                run = p.add_run()
                run.add_picture('paper_assets/arch.png', width=Inches(3.3))
                cap = doc.add_paragraph('Fig. 1: Overall System Architecture of Vayu Drishti')
                cap.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
                cap.runs[0].font.italic = True
                cap.runs[0].font.name = 'Times New Roman'
                cap.runs[0].font.size = Pt(9)
                p._p.addnext(cap._p)

        elif "Fig.2 :" in text or "Fig.2:" in text:
            p.text = ""
            if os.path.exists('paper_assets/ml_pipe.png'):
                run = p.add_run()
                run.add_picture('paper_assets/ml_pipe.png', width=Inches(3.3))
                cap = doc.add_paragraph('Fig. 2: Dual-Model Video Processing Pipeline (YOLOv11n & RescueNet)')
                cap.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
                cap.runs[0].font.italic = True
                cap.runs[0].font.name = 'Times New Roman'
                cap.runs[0].font.size = Pt(9)
                p._p.addnext(cap._p)

        elif "Fig.3 :" in text or "Fig.3:" in text:
            p.text = ""
            if os.path.exists('paper_assets/ws_flow.png'):
                run = p.add_run()
                run.add_picture('paper_assets/ws_flow.png', width=Inches(3.3))
                cap = doc.add_paragraph('Fig. 3: WebSocket Communication Flow and CesiumJS Mapping')
                cap.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
                cap.runs[0].font.italic = True
                cap.runs[0].font.name = 'Times New Roman'
                cap.runs[0].font.size = Pt(9)
                p._p.addnext(cap._p)

    doc.save(output_path)
    print(f"Diagrams successfully inserted into {output_path}")

if __name__ == '__main__':
    insert_diagrams('Vayu-Drishti.docx', 'Vayu-Drishti.docx')
