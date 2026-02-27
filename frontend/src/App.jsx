import React, { useMemo, useEffect, useState, useRef } from 'react';
import { Viewer, Entity } from "resium";
import * as Cesium from "cesium"; 
import { Cartesian3, HermitePolynomialApproximation, Color } from "cesium";
import useWebSocket from './hooks/useWebSocket';

import LeftSidebar from './components/LeftSideBar'
import RightSidebar from './components/RightSidebar';

function App() {
  const viewerRef = useRef(null);
  const [isTracked, setIsTracked] = useState(true);
  const [disasterEvents, setDisasterEvents] = useState([]);

  // Use explicit IP to match your backend logs
  const telemetry = useWebSocket('ws://127.0.0.1:8000/ws/telemetry/');

  useEffect(()=> {
    const fetchDisasterData = async() => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/survivors/');
        if(!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setDisasterEvents(data.features || []);
        console.log("Project Vayu Drishti Data Received: ", data);
      }
      catch(error) {
        console.error("API connection failed", error);
      }
    };
    fetchDisasterData();
  }, []);

  const dronePosition = useMemo(() => {
    if (telemetry?.latitude && telemetry?.longitude) {
      return Cartesian3.fromDegrees(telemetry.longitude, telemetry.latitude, telemetry.altitude || 100);
    }
    return Cartesian3.fromDegrees(78.4867, 17.3850, 100); 
  }, [telemetry]);

  return (
    <div style = {{display:'flex', height: "100vh", width:"100vw", backgroundColor:"#1e1e1e", color:"white", overflow: 'hidden'}}>
      
      {/* 1. LEFT SIDEBAR: FILTERS */}
      <LeftSidebar />

      {/* ============== CENTER: The Master Map ==============*/}
      <div style={{ flexGrow: 1, position: 'relative' }}>
        {/* Top Overlay HUD */}
        <div style={{ position: 'absolute', top: 15, left: 15, zIndex: 10, background: 'rgba(0,0,0,0.8)', padding: '10px 20px', borderRadius: '8px', border: '1px solid #333' }}>
          <h1 style={{ margin: 0, fontSize: '1.5rem', color: '#00ffcc' }}>Project Vayu Drishti</h1>
          <p style={{ margin: '5px 0 0 0', fontSize: '0.9rem', color: '#ccc' }}>
            Active Database Events: {disasterEvents.length}
          </p>
        </div>

        {/* Cesium 3D Globe */}
        <Viewer 
          full 
          animation={false} 
          timeline={false} 
          ref={viewerRef}
          onMouseDown={() => setIsTracked(false)} // Unlock camera on user click
        >
          {/* The Drone Entity */}
          <Entity
            name="Alpha-1"
            position={dronePosition}
            label={{ 
            text: "Alpha-1", 
            font: "14px monospace", 
            fillColor: Cesium.Color.LIME,
            outlineColor: Cesium.Color.BLACK,
            outlineWidth: 2,
            verticalOrigin: Cesium.VerticalOrigin.BOTTOM, 
            pixelOffset: new Cesium.Cartesian2(0, -20) 
          }}
            point={{ pixelSize: 20, color: Cesium.Color.RED }}
            tracked={isTracked}
            interpolationAlgorithm={HermitePolynomialApproximation}
            interpolationDegree={2}
          />

          {/* THE SEEDED DISASTER EVENTS (Yellow Dots) */}
          {disasterEvents.map((event, index)=> {
            if(!event?.geometry?.coordinates) return null;
            const [lng, lat] = event.geometry.coordinates;
            return (
              <Entity
                key={index}
                position={Cartesian3.fromDegrees(lng, lat)}
                point={{ pixelSize: 8, color: Color.YELLOW}}
                name={`Event ID: ${index}`}
              />
            );
          })}
        </Viewer>
      </div>

      {/* 2. RIGHT SIDEBAR: FLEET MANAGER */}
      <RightSidebar 
        telemetry={telemetry} 
        onTrack={() => setIsTracked(true)} 
        isTracked={isTracked} 
      />
    </div>
  );
}

export default App;