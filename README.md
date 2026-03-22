# 🚁 Project Vayu Drishti (AMRIT)

## 📝 About the Project
**Project Vayu Drishti** (Advanced Management & Rescue using Intelligent Telemetry) is a real-time, 3D disaster assessment and management dashboard. Built to handle complex geographic data, it processes autonomous drone footage to map survivor clusters and damage reports on a live 3D globe, enabling rapid and informed decision-making for commanders on the ground.

## 🎯 Goals & Objectives
- **Real-Time Telemetry:** Track active drone fleets with sub-second latency using WebSockets.
- **Geospatial Visualization:** Render precise 3D maps of disaster zones using CesiumJS, allowing commanders to view topography and infrastructure.
- **Data-Driven Rescue:** Map algorithmically detected "Survivor Clusters" and "Damage Reports" (fires, floods, collapsed structures) directly onto the interactive globe.
- **Single-Pane-of-Glass UI:** Prevent screen fatigue by providing a "God's Eye" view where all critical disaster data is layered on a single, filterable map.

## 🏗️ Tech Stack
- **Frontend:** React, Resium, CesiumJS (for 3D globe rendering)
- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL + PostGIS (GeoDjango for advanced spatial queries)
- **Real-Time Engine:** Django Channels, Redis, WebSockets
- **Simulation Environment:** Custom Python scripts for generating localized disaster zones and live drone flight paths.

---

## 🛠️ Setup Instructions

### Prerequisites
Before setting up the project locally, ensure your system has the following installed:
- **Python 3.10+**
- **Node.js & npm**
- **PostgreSQL** (with the **PostGIS** extension enabled)
- **Docker** (required for running the Redis server)

---

### 1. Backend Setup (The Brain & Radio Tower)
The backend handles the PostGIS database, the REST API, and the WebSocket connections.

```bash
# Clone the repository and navigate to the backend directory
git clone <your-repo-url>
cd vayu-drishti/backend

# Create and activate a virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate  
# On Windows:
venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start Redis for WebSockets (using Docker)
docker run -p 6379:6379 -d redis:7

# Apply database migrations to set up PostGIS tables
python manage.py migrate

# 🚨 CRITICAL: Seed the database with simulation data
# This generates 50 dummy survivors/fires in the Godavarikhani region for UI testing
python manage.py seed_disaster

# Start the Django development server
python manage.py runserver
```
---
### 2. Frontend Setup (The 3D Dashboard)
The frontend connects to the Django API and visualizes the disaster data on a 3D globe.
Open a second terminal window:

```
# Navigate to the frontend directory
cd vayu-drishti/frontend

# Install node modules
npm install

# Start the React development server
npm run dev  # (or npm start, depending on your package.json)
```
---
### 3. Running the Drone Simulation (Live Telemetry)
To test the real-time WebSocket architecture, we use a simulation script that mimics a drone flying over the disaster zone, sending coordinates 10 times a second.
Open a third terminal window (ensure your Python venv is active):

```
# Navigate to the root of the project where the script is located
python fake_drone.py
```
---


---
---
## These commands are for feat/integarting branch only
```
# Start the Celery worker in vayu-drishti-ml for tasks.py
"venv\Scripts\python.exe" -m celery -A tasks worker --loglevel=info --pool=solo

# Start the Django Server
python manage.py runserver

# Start bridge_listener.py in vayu-drishti-web Backend
python bridge_listener.py

# Start react server in vayu-drishti-web Frontend
npm run dev

# Start trigger_test.py in vayu-drishti-ml
python trigger_test.py

# Need to set the path of the video in trigger_test.py for the destroyed_town.mp4

```

---
---
## commands for feature/routing-and-drone branch
```
# The steps to run the servers and workers are identical to the integrating branch.
# Start the Celery worker in vayu-drishti-ml for tasks.py
"venv\Scripts\python.exe" -m celery -A tasks worker --loglevel=info --pool=solo

# Start the Django Server
cd backend && python manage.py runserver

# Start bridge_listener.py in vayu-drishti-web Backend
cd backend && python bridge_listener.py

# Start react server in vayu-drishti-web Frontend
cd frontend && npm run dev

# Using fake_drone.py with new realistic mock path simulation:
# You can customize start_lat, start_lng, and duration respectively.
python fake_drone.py 17.3850 78.4867 60

### 🗺️ Advanced Routing Feature

The new **Routing Feature** calculates the safest and most optimal path for rescue forces to reach detected survivor clusters, fully accounting for real-time segmented damage zones using the **RescueNet** dataset classification.

#### How It Works:
1. As the ML pipeline (`trigger_test.py` or live drone feed) processes data, bounding boxes and segmentations are broadcasted to the frontend via WebSockets.
2. The UI lists detected **Survivor Clusters** dynamically in the Emergency Routing panel on the left.
3. Users click **"Calculate Safe Route"** for a specific cluster.
4. The backend initiates a **Grid-based A*** algorithm using the `networkx`, `numpy`, and `shapely` Python libraries.

#### Algorithm Specifications:
- **Algorithm:** Grid-based A* Search Algorithm.
- **Heuristic:** Euclidean Distance (`sqrt((x1-x2)^2 + (y1-y2)^2)`).
- **Grid Resolution:** ~10 meters per grid cell (`0.0001` degrees).
- **Obstacle Buffer Radius:** ~20 meters (`0.0002` degrees).

#### Obstacle Avoidance Matrix (RescueNet Dataset):
The algorithm dynamically queries the PostGIS database for all `DamageReport` geometries. Based on the RescueNet classification, it determines whether a segment is safely traversable or must be avoided:

**🚫 Obstacles (Treated as Impassable):**
- `WATER` (Natural or Flood)
- `BUILDING_MINOR_DAMAGE`
- `BUILDING_MAJOR_DAMAGE`
- `BUILDING_TOTAL_DESTRUCTION`
- `VEHICLE`
- `ROAD_BLOCKED`
- `TREE`
- `POOL`

**✅ Safe Zones (Permitted for Routing):**
- `BUILDING_NO_DAMAGE`
- `ROAD_CLEAR`

If a route is successfully found around the obstacles, it is transmitted back to the frontend and visualized as a glowing cyan polyline over the 3D CesiumJS globe.
```
