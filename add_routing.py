import docx
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_routing_section(filepath, output_path):
    doc = docx.Document(filepath)

    # We want to find a good spot under the "System Architecture" or "Pipeline" section
    # Let's look for "III. REAL-TIME COMMUNICATION" or a similar heading and insert before it
    # Or just after the ML pipeline description.

    insert_idx = -1
    for i, p in enumerate(doc.paragraphs):
        # We find a logical place to insert this subsection
        if p.text.startswith("V.  RESULTS AND ANALYSIS"):
            insert_idx = i
            break

    if insert_idx != -1:
        # We will insert paragraphs before the RESULTS section to cover Routing

        # Helper to create a formatted paragraph
        def create_heading(text, level=2):
            new_p = doc.paragraphs[insert_idx].insert_paragraph_before()
            run = new_p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10) if level > 1 else Pt(10)
            run.font.bold = True
            return new_p

        def create_paragraph(text):
            new_p = doc.paragraphs[insert_idx].insert_paragraph_before()
            new_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            run = new_p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
            return new_p

        create_heading("D. Grid-Based A* Routing Engine and Django Backend")
        create_paragraph(
            "While YOLOv11n and RescueNet provide vital intelligence regarding survivor locations and infrastructural damage, the true operational value of VAYU-DRISHTI lies in transforming this raw data into actionable ground-level guidance. This is achieved through our highly specialized Django-based routing backend, which utilizes a Grid-Based A* (A-Star) search algorithm."
        )
        create_paragraph(
            "1) PostGIS Geometry Integration: As the RescueNet segmentation model classifies areas into distinct damage categories (e.g., 'Building Major Damage', 'Road Blocked'), these semantic masks are vectorized into precise geographic polygons. These polygons are instantaneously persisted into a PostGIS-enabled PostgreSQL database alongside the drone's telemetry."
        )
        create_paragraph(
            "2) Dynamic Hazard Buffering: The routing engine, implemented using Python's NetworkX and Shapely libraries, treats these severe damage classifications as impassable zones. To ensure maximum safety for deployed rescue teams, the engine dynamically applies a 20-meter exclusion buffer around all polygons flagged as hazardous. This mathematical inflation prevents the algorithm from computing paths that skirt dangerously close to unstable structures or flooded routes."
        )
        create_paragraph(
            "3) Real-Time Path Computation: When a survivor cluster is detected by YOLOv11n, the A* algorithm is triggered. It computes the shortest, safest route from a designated safe-zone dispatch point to the survivor's coordinates, strictly navigating around the dynamically generated 20-meter hazard buffers. Operating within the asynchronous Django Channels framework, this computation happens in milliseconds. The finalized safe path is serialized as a GeoJSON polyline and broadcasted via Redis Pub/Sub directly to the CesiumJS 3D dashboard, allowing command center operators to guide ground teams precisely and safely in real-time."
        )

        doc.save(output_path)
        print(f"Routing section successfully injected before paragraph {insert_idx}.")
    else:
        print("Could not find appropriate insertion point.")

if __name__ == '__main__':
    add_routing_section('Vayu-Drishti-IEEE (1).docx', 'Vayu-Drishti-IEEE (1).docx')
