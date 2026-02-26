import React, { useEffect, useState } from 'react';
import { Viewer, Entity } from "resium";
import { Cartesian3, Color } from "cesium";
import useWebSocket from './hooks/useWebSocket';

// Hardcoded GPS coordinate for the drone (Hyderabad area)
const initialDronePosition = Cartesian3.fromDegrees(79.485, 18.805, 300); 

function App() {

  const [survivors, setSurvivors] = useState([]);
  const [damageReports, setDamageReports] = useState([]);
  const [activeDrones, setActiveDrones] = useState([]);

  const [showSurvivors, setShowSurvivors] = useState(true);
  const [showDamage, setShowDamage] = useState(true);
  const [damageFilters, setDamageFilters] = useState({ FIRE: true, FLOOD: true });
  const [showDrones, setShowDrones] = useState(true);

  // Maintain WebSocket and update activeDrones on incoming telemetry
  useWebSocket('ws://localhost:8000/ws/telemetry/', (data) => {
    if (!data) return;
    if (data.lat != null && data.lng != null) {
      setActiveDrones(prev => {
        const idx = prev.findIndex(d => d.id === data.id);
        if (idx === -1) return [...prev, data];
        const copy = [...prev]; copy[idx] = { ...copy[idx], ...data }; return copy;
      });
    }
  });

  useEffect(()=> {
    const fetchDisasterData = async() => {
      try {
        const [sRes, dRes] = await Promise.all([
          fetch('http://127.0.0.1:8000/api/survivors/'),
          fetch('http://127.0.0.1:8000/api/damage/'),
        ]);

        if(!sRes.ok || !dRes.ok) {
          throw new Error(`HTTP error! status: ${sRes.status} / ${dRes.status}`);
        }

        const sJson = await sRes.json();
        const dJson = await dRes.json();

        setSurvivors(sJson.features || []);
        setDamageReports(dJson.features || []);

        console.log("Project Vayu Drishti Data Received: ", { survivors: sJson, damage: dJson });
        console.log(`Found ${sJson.features?.length} survivors, ${dJson.features?.length} damage events`);

      }
      catch(error) {
        console.error("API connection failed", error);
      }
    };
    fetchDisasterData();
  }, []);

  return (
    <div style = {{display:'flex', height: "100vh", width:"100vw", backgroundColor:"#1e1e1e", color:"white"}}>
      <div style = {{width:"250px", padding:"20px", borderRight:"1px solid #333", display:"flex", flexDirection:"column"}}>
        <h2 style={{ fontSize:'1.2rem', marginBottom:'20px', borderBottom:'1px solid #444', paddingBottom:'10px'}}>Filters</h2>
        <div style={{ color:'#aaa', lineHeight:'2'}}>
          <label style={{ display:'block' }}>
            <input type='checkbox' checked={showSurvivors} onChange={e => setShowSurvivors(e.target.checked)} /> Survivor Clusters
          </label>

          <label style={{ display:'block' }}>
            <input type='checkbox' checked={showDamage} onChange={e => setShowDamage(e.target.checked)} /> Damage Reports
          </label>

          {showDamage && (
            <div style={{ paddingLeft: '14px', color: '#bbb' }}>
              <label style={{ display:'block' }}>
                <input type='checkbox' checked={damageFilters.FIRE} onChange={e => setDamageFilters(prev => ({...prev, FIRE: e.target.checked}))} /> Fire
              </label>
              <label style={{ display:'block' }}>
                <input type='checkbox' checked={damageFilters.FLOOD} onChange={e => setDamageFilters(prev => ({...prev, FLOOD: e.target.checked}))} /> Flood
              </label>
            </div>
          )}

          <label style={{ display:'block' }}>
            <input type='checkbox' checked={showDrones} onChange={e => setShowDrones(e.target.checked)} /> Active Drones
          </label>
        </div>
    </div>

    {/* ============== CENTER: The Master Map ==============*/}
    <div style={{ flexGrow: 1, position: 'relative' }}>
      {/* Top Overlay HUD */}
      <div style={{ position: 'absolute', top: 15, left: 15, zIndex: 10, background: 'rgba(0,0,0,0.8)', padding: '10px 20px', borderRadius: '8px', border: '1px solid #333' }}>
        <h1 style={{ margin: 0, fontSize: '1.5rem', color: '#00ffcc' }}>Project Vayu Drishti</h1>
        <p style={{ margin: '5px 0 0 0', fontSize: '0.9rem', color: '#ccc' }}>
          Active Database Events: {survivors.length + damageReports.length}
        </p>
      </div>

      {/* Cesium 3D Globe */}
      <Viewer full animation={false} timeline={false}>
        {/* Fallback single drone (kept for initial view) */}
        {(!activeDrones || activeDrones.length === 0) && showDrones && (
          <Entity
            position={initialDronePosition}
            point={{ pixelSize: 12, color: Color.RED, outlineColor: Color.WHITE, outlineWidth: 2 }}
            name="Drone Alpha-1"
            description="Autonomous Survey Drone"
            tracked={true}
          />
        )}

        {/* Survivor Clusters */}
        {showSurvivors && survivors.map((f, idx) => {
          if(!f?.geometry?.coordinates) return null;
          const [lng, lat] = f.geometry.coordinates;
          const props = f.properties || {};
          return (
            <Entity
              key={`surv-${idx}`}
              position={Cartesian3.fromDegrees(lng, lat)}
              point={{ pixelSize: 6, color: Color.LIME}}
              name={`Survivor ${props.id || idx}`}
              description={`Count: ${props.estimated_count}, Confidence: ${props.confidence_score}%`}
            />
          );
        })}

        {/* Damage Reports with sub-filters */}
        {showDamage && (() => {
          const damageColor = (type) => {
            if (type === 'FIRE') return Color.RED;
            if (type === 'FLOOD') return Color.BLUE;
            return Color.ORANGE;
          };

          return damageReports.filter(d => {
            const t = d.properties?.damage_type;
            if (!t) return true;
            if (t === 'FIRE') return damageFilters.FIRE;
            if (t === 'FLOOD') return damageFilters.FLOOD;
            return true;
          }).map((f, idx) => {
            if(!f?.geometry?.coordinates) return null;
            const [lng, lat] = f.geometry.coordinates;
            const t = f.properties?.damage_type;
            const color = damageColor(t);
            return (
              <Entity
                key={`damage-${idx}`}
                position={Cartesian3.fromDegrees(lng, lat)}
                point={{ pixelSize: 8, color: color}}
                name={`Damage ${f.id || idx}`}
                description={`Type: ${t}, Severity: ${f.properties?.severity_level}`}
              />
            );
          });
        })()}

        {/* Active Drones from telemetry */}
        {showDrones && activeDrones.map((d, i) => {
          if (d.lat == null || d.lng == null) return null;
          return (
            <Entity
              key={`drone-${d.id || i}`}
              position={Cartesian3.fromDegrees(d.lng, d.lat, d.alt || 200)}
              point={{ pixelSize: 12, color: Color.RED, outlineColor: Color.WHITE, outlineWidth: 2 }}
              name={`Drone ${d.id || i}`}
              description="Live Telemetry"
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
    // <div style={{ height: "100vh", width: "100vw" }}>
    //   {/* Text Overlay */}
    //   <div style={{ position: 'absolute', top: 10, left: 10, zIndex: 10, color: 'white', background: 'rgba(0,0,0,0.5)', padding: '10px' }}>
    //     <h1>Vayu-Drishti Dashboard</h1>
    //     <p>Telemetry Status: Connected (Check Console)</p>
    //   </div>

    //   {/* Cesium Globe with Entity and Auto-Camera */}
    //   <Viewer full>
    //     <Entity
    //       position={dronePosition}
    //       point={{ pixelSize: 20, color: Color.red }} 
    //       description="Static Drone Entity"
    //       selected={true} // This highlights the entity
    //       tracked={true}  // This tells the camera to follow it
    //     />
    //   </Viewer>
    // </div>
  );
}

export default App;