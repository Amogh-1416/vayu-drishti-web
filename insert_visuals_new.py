import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def insert_diagrams(filepath, output_path):
    doc = docx.Document(filepath)

    for i, p in enumerate(doc.paragraphs):
        text = p.text.strip()

        # Fig 1. System Architecture
        if "Fig. 1.  Overall System Architecture" in text:
            if os.path.exists('assets/arch.png'):
                run = p.add_run()
                run.add_picture('assets/arch.png', width=Inches(6.0))
                # Add picture before the text placeholder to match typical IEEE caption formatting (image then caption below)
                p._p.insert(0, run._r)

        # Fig 2. ML Pipeline
        elif "Fig. 2.  Dual-Model Video Processing Pipeline" in text:
            if os.path.exists('assets/ml_pipe.png'):
                run = p.add_run()
                run.add_picture('assets/ml_pipe.png', width=Inches(6.0))
                p._p.insert(0, run._r)

        # Fig 3. WebSocket Flow
        elif "Fig. 3.  WebSocket Communication Flow" in text:
            if os.path.exists('assets/ws_flow.png'):
                run = p.add_run()
                run.add_picture('assets/ws_flow.png', width=Inches(6.0))
                p._p.insert(0, run._r)

        # Fig 4. Matplotlib Loss Graph
        elif "Fig. 4.  YOLOv11n Training Loss" in text:
            if os.path.exists('assets/yolo_loss.png'):
                run = p.add_run()
                run.add_picture('assets/yolo_loss.png', width=Inches(4.5))
                p._p.insert(0, run._r)

        # Fig 5. Matplotlib Accuracy Graph
        elif "Fig. 5.  YOLOv11-Seg Loss" in text:
            if os.path.exists('assets/seg_acc.png'):
                run = p.add_run()
                run.add_picture('assets/seg_acc.png', width=Inches(4.5))
                p._p.insert(0, run._r)

    doc.save(output_path)
    print(f"All 5 visual diagrams successfully inserted into {output_path}")

if __name__ == '__main__':
    insert_diagrams('Vayu-Drishti-IEEE (1).docx', 'Vayu-Drishti-IEEE (1).docx')
