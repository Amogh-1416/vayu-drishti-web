import React from 'react';
import { Viewer, Entity } from "resium";
import { Cartesian3 } from "cesium";
import useWebSocket from './hooks/useWebSocket';

// Hardcoded GPS coordinate for the drone (Hyderabad example)
const dronePosition = Cartesian3.fromDegrees(78.4867, 17.3850, 100); 

function App() {
  // Maintain your WebSocket connection from Issue #11
  useWebSocket('ws://localhost:8000/ws/telemetry/');

  return (
    <div style={{ height: "100vh", width: "100vw" }}>
      {/* Text Overlay */}
      <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 10, color: 'white', background: 'rgba(0,0,0,0.5)', padding: '10px' }}>
        <h1>Vayu-Drishti Dashboard</h1>
        <p>Telemetry Status: Connected (Check Console)</p>
      </div>

      {/* Cesium Globe with Entity */}
      <Viewer full>
        <Entity
          position={dronePosition}
          point={{ pixelSize: 15, color: "red" }} // Represents the drone
          description="Static Drone Entity"
        />
      </Viewer>
    </div>
  );
}

export default App;