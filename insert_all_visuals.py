import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def insert_diagrams(filepath, output_path):
    doc = docx.Document(filepath)

    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()

        # Fig 1. System Architecture
        if "Fig. 1: System Architecture" in text or "Fig.1:" in text:
            p.text = ""
            if os.path.exists('paper_assets/arch.png'):
                run = p.add_run()
                run.add_picture('paper_assets/arch.png', width=Inches(6.0)) # Large width
                cap = doc.add_paragraph('Fig. 1: Overall System Architecture of Vayu Drishti')
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cap.runs[0].font.italic = True
                cap.runs[0].font.name = 'Times New Roman'
                cap.runs[0].font.size = Pt(9)
                p._p.addnext(cap._p)

        # Fig 2. ML Pipeline
        elif "Fig. 2: Dual-Model Video Processing Pipeline" in text or "Fig.2:" in text:
            p.text = ""
            if os.path.exists('paper_assets/ml_pipe.png'):
                run = p.add_run()
                run.add_picture('paper_assets/ml_pipe.png', width=Inches(6.0))
                cap = doc.add_paragraph('Fig. 2: Dual-Model Video Processing Pipeline (YOLOv11n & RescueNet)')
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cap.runs[0].font.italic = True
                cap.runs[0].font.name = 'Times New Roman'
                cap.runs[0].font.size = Pt(9)
                p._p.addnext(cap._p)

        # Fig 3. WebSocket Flow
        elif "Fig. 3: WebSocket Communication Flow" in text or "Fig.3:" in text:
            p.text = ""
            if os.path.exists('paper_assets/ws_flow.png'):
                run = p.add_run()
                run.add_picture('paper_assets/ws_flow.png', width=Inches(6.0))
                cap = doc.add_paragraph('Fig. 3: WebSocket Communication Flow and CesiumJS Mapping')
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cap.runs[0].font.italic = True
                cap.runs[0].font.name = 'Times New Roman'
                cap.runs[0].font.size = Pt(9)
                p._p.addnext(cap._p)

        # Fig 4. Matplotlib Loss Graph
        elif text.startswith("Fig.4") or "Fig.4 :" in text:
            p.text = ""
            if os.path.exists('paper_assets/yolo_loss.png'):
                run = p.add_run()
                run.add_picture('paper_assets/yolo_loss.png', width=Inches(4.5))
                cap = doc.add_paragraph('Fig. 4: YOLOv11n Object Detection Training Loss over 25 Epochs')
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cap.runs[0].font.italic = True
                cap.runs[0].font.name = 'Times New Roman'
                cap.runs[0].font.size = Pt(9)
                p._p.addnext(cap._p)

        # Fig 5. Matplotlib Accuracy Graph
        elif text.startswith("Fig.5") or "Fig.5 :" in text:
            p.text = ""
            if os.path.exists('paper_assets/rescuenet_acc.png'):
                run = p.add_run()
                run.add_picture('paper_assets/rescuenet_acc.png', width=Inches(4.5))
                cap = doc.add_paragraph('Fig. 5: RescueNet Semantic Segmentation mIoU Convergence')
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cap.runs[0].font.italic = True
                cap.runs[0].font.name = 'Times New Roman'
                cap.runs[0].font.size = Pt(9)
                p._p.addnext(cap._p)

    doc.save(output_path)
    print(f"All 5 visual diagrams successfully inserted into {output_path} at large scale.")

if __name__ == '__main__':
    insert_diagrams('Vayu-Drishti.docx', 'Vayu-Drishti.docx')
