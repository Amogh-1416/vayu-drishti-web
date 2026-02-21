import React from 'react';
import useWebSocket from './hooks/useWebSocket';
// Keep your Cesium imports here if you want the globe to stay

function App() {
  // Use the URL from your assigned GitHub issue
  useWebSocket('ws://localhost:8000/ws/telemetry');

  return (
    <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 10, color: 'white', background: 'rgba(0,0,0,0.5)', padding: '10px' }}>
      <h1>Vayu-Drishti Dashboard</h1>
      <p>Telemetry Status: Connected (Check Console)</p>
    </div>
    // Your Globe component would go here
  );
}

export default App;