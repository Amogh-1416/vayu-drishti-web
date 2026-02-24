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
