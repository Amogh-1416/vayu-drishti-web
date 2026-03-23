import os
import subprocess

def create_mermaid_files():
    os.makedirs('paper_assets', exist_ok=True)

    # Diagram 1: Overall System Architecture
    arch = """graph TD
    subgraph UAV Layer
        A[Drone / UAV] -->|Video & Telemetry| B(Django Backend)
    end

    subgraph Processing Layer
        B -->|Image Frames| C{YOLOv11n Detection}
        B -->|Image Frames| D{RescueNet Segmentation}
        C -->|Bounding Boxes| E[PostGIS Database]
        D -->|Damage Polygons| E
        E -->|Map Data| F[Routing Engine]
        F -->|Waypoints| B
    end

    subgraph Presentation Layer
        B <-->|WebSockets| G[React + CesiumJS Dashboard]
    end
    """

    with open('paper_assets/arch.mmd', 'w') as f:
        f.write(arch)

    # Diagram 2: Machine Learning Data Pipeline
    ml_pipe = """graph LR
    A[Raw Video Feed] --> B[Frame Extraction]
    B --> C[Preprocessing]
    C --> D[YOLOv11n Model]
    C --> E[RescueNet Model]
    D --> F[Human Detection Confidence > 0.5]
    E --> G[Semantic Masks: Safe vs Impassable]
    F --> H[Aggregation]
    G --> H
    H --> I[JSON Output to DB]
    """

    with open('paper_assets/ml_pipe.mmd', 'w') as f:
        f.write(ml_pipe)

    # Diagram 3: Real-Time WebSocket Communication Flow
    ws_flow = """sequenceDiagram
    participant UAV
    participant Django as Django Channels
    participant Redis as Redis Pub/Sub
    participant Dashboard as React Client

    UAV->>Django: Send Telemetry (JSON)
    Django->>Redis: Publish Message to 'drone_telemetry'
    Redis-->>Django: Receive Message
    Django->>Dashboard: Broadcast via WebSocket
    Dashboard-->>Django: Acknowledge
    """

    with open('paper_assets/ws_flow.mmd', 'w') as f:
        f.write(ws_flow)

def generate_images():
    # Use mmdc to convert to png
    files = ['arch.mmd', 'ml_pipe.mmd', 'ws_flow.mmd']
    for file in files:
        base = file.split('.')[0]
        cmd = f"mmdc -i paper_assets/{file} -o paper_assets/{base}.png -w 1200 -b white"
        print(f"Running: {cmd}")
        # Note: Added --puppeteerConfigFile if running as root/sandbox causes issues, but typically fine.
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error generating {file}:\n{result.stderr}")
        else:
            print(f"Successfully generated {base}.png")

if __name__ == "__main__":
    create_mermaid_files()
    generate_images()
