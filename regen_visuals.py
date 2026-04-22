import os
import subprocess

def create_mermaid_files():
    os.makedirs('paper_assets', exist_ok=True)

    # Diagram 1: Overall System Architecture (Simplified and Large text)
    arch = """graph TD
    classDef primary fill:#4A90E2,stroke:#000,stroke-width:2px,color:#fff,rx:5px,ry:5px,font-size:24px;
    classDef secondary fill:#50E3C2,stroke:#000,stroke-width:2px,color:#000,rx:5px,ry:5px,font-size:24px;
    classDef database fill:#F5A623,stroke:#000,stroke-width:2px,color:#fff,rx:5px,ry:5px,font-size:24px;
    classDef frontend fill:#E91E63,stroke:#000,stroke-width:2px,color:#fff,rx:5px,ry:5px,font-size:24px;

    subgraph "Edge Device (UAV)"
        A[UAV / Drone<br>Telemetry & Camera]:::primary
    end

    subgraph "Backend Processing Pipeline"
        B[Django Channels<br>WebSocket Server]:::secondary
        C[YOLOv11n<br>Human Detection]:::secondary
        D[RescueNet<br>Damage Segmentation]:::secondary
        E[(PostGIS Spatial DB)]:::database
        F[Grid-Based A*<br>Routing Engine]:::secondary
    end

    subgraph "Command Center (Frontend)"
        G[React + CesiumJS<br>3D Dashboard]:::frontend
    end

    A -- "Live Video & GPS" --> B
    B -- "Frames" --> C
    B -- "Frames" --> D
    C -- "Survivor Coordinates" --> E
    D -- "Damage Polygons" --> E
    E -- "Geo Data" --> F
    F -- "Safe Paths" --> E
    B -- "Real-Time Updates" --> G
    E -- "Map Initialization" --> G
    """

    with open('paper_assets/arch.mmd', 'w') as f:
        f.write(arch)

    # Diagram 2: Machine Learning Data Pipeline
    ml_pipe = """graph LR
    classDef input fill:#9b59b6,stroke:#000,stroke-width:2px,color:#fff,font-size:24px;
    classDef process fill:#3498db,stroke:#000,stroke-width:2px,color:#fff,font-size:24px;
    classDef model fill:#e67e22,stroke:#000,stroke-width:2px,color:#fff,font-size:24px;
    classDef output fill:#2ecc71,stroke:#000,stroke-width:2px,color:#fff,font-size:24px;

    A([Raw Video Stream]):::input --> B["Frame Extractor (FPS Limit)"]:::process
    B --> C["Image Normalization & Resize"]:::process

    C --> D{"YOLOv11n (Heridal)"}:::model
    C --> E{"RescueNet"}:::model

    D -- Bounding Boxes --> F["Confidence Filter > 0.6"]:::process
    E -- Semantic Masks --> G["Polygon Vectorization"]:::process

    F --> H(["Survivor JSON Coordinates"]):::output
    G --> I(["Damage JSON Geometries"]):::output
    """

    with open('paper_assets/ml_pipe.mmd', 'w') as f:
        f.write(ml_pipe)

    # Diagram 3: Real-Time WebSocket Communication Flow
    ws_flow = """sequenceDiagram
    autonumber
    participant D as UAV Drone
    participant W as Django WebSocket Server
    participant R as Redis Pub/Sub
    participant F as React / CesiumJS Client

    D->>W: Connect (ws://api/drone/id/)
    W->>R: Subscribe to group 'drone_telemetry'
    F->>W: Connect (ws://api/dashboard/)
    W->>R: Subscribe to group 'drone_telemetry'

    loop Real-Time Telemetry Loop
        D->>W: Send JSON {lat, lng, alt, heading}
        W->>R: ChannelLayer.group_send()
        R-->>W: Broadcast Message
        W->>F: Send JSON {lat, lng, alt, heading}
        F->>F: Update Cesium 3D Entity Position
    end
    """

    with open('paper_assets/ws_flow.mmd', 'w') as f:
        f.write(ws_flow)

def generate_images():
    files = ['arch.mmd', 'ml_pipe.mmd', 'ws_flow.mmd']
    for file in files:
        base = file.split('.')[0]
        # Force a white background (-b white) and a massive scale (-s 5) for word doc clarity
        cmd = f"mmdc -i paper_assets/{file} -o paper_assets/{base}.png -t neutral -b white -s 5"
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error generating {file}:\n{result.stderr}")
        else:
            print(f"Successfully generated {base}.png")

if __name__ == "__main__":
    create_mermaid_files()
    generate_images()
