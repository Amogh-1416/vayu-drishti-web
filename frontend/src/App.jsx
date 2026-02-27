import React, { useMemo, useEffect, useState } from 'react';
import { Viewer, Entity } from "resium";
import * as Cesium from "cesium"; // Fixes: "Cesium is not defined"
import { Cartesian3, HermitePolynomialApproximation, Color } from "cesium";
import useWebSocket from './hooks/useWebSocket';

function App() {
  // Use explicit IP to match your backend logs
  const telemetry = useWebSocket('ws://127.0.0.1:8000/ws/telemetry/');
    const [disasterEvents, setDisasterEvents] = useState([]);

  // Maintaining WebSocket from Issue #11
  useWebSocket('ws://localhost:8000/ws/telemetry/');

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
        console.log(`Found ${data.features?.length} disaster events on the map`);

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
    <div style = {{display:'flex', height: "100vh", width:"100vw", backgroundColor:"#1e1e1e", color:"white"}}>
      <div style = {{width:"250px", padding:"20px", borderRight:"1px solid #333", display:"flex", flexDirection:"column"}}>
        <h2 style={{ fontSize:'1.2rem', marginBottom:'20px', borderBottom:'1px solid #444', paddingBottom:'10px'}}>Filters</h2>
        <div style={{ color:'#aaa', lineHeight:'2'}}>
          <label style={{ display:'block' }}><input type='checkbox' disabled checked />Survivor Clusters</label>
          <label style={{ display:'block' }}><input type='checkbox' disabled checked />Damage Reports</label>
          <label style={{ display:'block' }}><input type='checkbox' disabled checked />Active Drones</label>
        </div>
    </div>

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
      <Viewer full animation={false} timeline={false}>
        {/* The Drone Entity */}
    
      <Entity
        position={dronePosition}
        point={{ pixelSize: 20, color: Cesium.Color.RED }}
        tracked={true}
        // Smooths out the 1-second updates into a glide
        interpolationAlgorithm={HermitePolynomialApproximation}
        interpolationDegree={2}
      />
    {/* THE SEEDED DISASTER EVENTS */}
        {disasterEvents.map((event, index)=> {
          if(!event?.geometry?.coordinates){
            return null;
          }
          const [lng, lat] = event.geometry.coordinates;
          const props = event.properties

          return (
            <Entity
              key={index}
              position={Cartesian3.fromDegrees(lng, lat)}
              point={{ pixelSize: 8, color: Color.YELLOW}}
              name={`Event ID: ${index}`}
              description={`Data: ${JSON.stringify(props)}`}
            />
          );
        })}
      </Viewer>
    </div>

    {/* RIGHT SIDEBAR: FLEET MANAGER */}
    <div style={{ width: '300px', padding: '20px', backgroundColor: '#1e1e1e', borderLeft: '1px solid #333' }}>
      <h2 style={{ fontSize: '1.2rem', marginBottom: '20px', borderBottom: '1px solid #444', paddingBottom: '10px' }}>
        Fleet Manager
      </h2>

      {/* Drone Statue Card */}
      <div style={{ background: '#2a2a2a', padding: '15px', borderRadius: '8px', marginBottom: '20px', border: '1px solid #444' }}>
        <h3 style={{ margin: '0 0 10px 0', fontSize: '1rem' }}>Alpha-1</h3>
        <p style={{ margin: 0, fontSize: '0.85rem', color: '#00ffcc' }}>● Telemetry Active</p>
      </div>
      <div style={{ width: '100%', height: '180px', background: '#000', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '8px', border: '1px solid #444' }}>
        <p style={{ color: '#555', margin: 0, fontSize: '0.9rem' }}>[ Camer Feed Offline ]</p>
      </div>
    </div>
    </div>
  );
}

export default App;