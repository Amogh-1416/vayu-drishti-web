import React, { useMemo, useEffect, useState, useRef } from 'react';
import { Viewer, Entity, ImageryLayer } from "resium";
import * as Cesium from "cesium"; 
import { Cartesian3, HermitePolynomialApproximation, Color } from "cesium";
import useWebSocket from './hooks/useWebSocket';

import LeftSidebar from './components/LeftSideBar'
import RightSidebar from './components/RightSidebar';

function App() {
  const viewerRef = useRef(null);
  const [isTracked, setIsTracked] = useState(true);
  
  // State for initial DB load
  const [disasterEvents, setDisasterEvents] = useState([]);
  
  // --- NEW: State for real-time AI detections ---
  const [liveSurvivors, setLiveSurvivors] = useState([]);
  const [liveDamage, setLiveDamage] = useState([]);
  const [esriProvider, setEsriProvider] = useState(null);

  // Routing State
  const [routePath, setRoutePath] = useState([]);
  const [calculatingRoute, setCalculatingRoute] = useState(false);
  const [routeError, setRouteError] = useState(null);

  // WebSockets
  const telemetry = useWebSocket('ws://127.0.0.1:8000/ws/telemetry/');
  const disasterUpdate = useWebSocket('ws://127.0.0.1:8000/ws/disaster/'); // Listen to the Bridge

  useEffect(() => {
    const loadMap = async () => {
      try {
        // Modern Cesium requires .fromUrl() to handle the Promise
        const provider = await Cesium.ArcGisMapServerImageryProvider.fromUrl(
          'https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer'
        );
        setEsriProvider(provider);
      } catch (err) {
        console.error("Failed to load Esri Satellite map:", err);
      }
    };
    loadMap();
  }, []);

  // Fetch initial data
  useEffect(() => {
    const fetchDisasterData = async() => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/survivors/');
        if(!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        setDisasterEvents(data.features || []);
      } catch(error) {
        console.error("API connection failed", error);
      }
    };
    fetchDisasterData();
  }, []);

  // --- NEW: Handle Incoming Real-Time Data ---
  useEffect(() => {
    if (!disasterUpdate) return;

    if (disasterUpdate.type === "SURVIVOR") {
      setLiveSurvivors((prev) => [...prev, disasterUpdate]);
    } else if (disasterUpdate.type === "DAMAGE") {
      setLiveDamage((prev) => [...prev, disasterUpdate]);
    }
  }, [disasterUpdate]);

  const dronePosition = useMemo(() => {
    if (telemetry?.latitude && telemetry?.longitude) {
      return Cartesian3.fromDegrees(telemetry.longitude, telemetry.latitude, telemetry.altitude || 100);
    }
    return Cartesian3.fromDegrees(78.4867, 17.3850, 100); 
  }, [telemetry]);

  const handleRouteRequest = async (survivor) => {
    setCalculatingRoute(true);
    setRouteError(null);
    try {
      // Assuming Rescue Base is at some static point (could be made dynamic)
      const rescueBase = { lat: 17.3840, lng: 78.4850 };

      const response = await fetch('http://127.0.0.1:8000/api/route/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          start_lat: rescueBase.lat,
          start_lng: rescueBase.lng,
          end_lat: survivor.lat,
          end_lng: survivor.lng
        })
      });

      const data = await response.json();
      if (response.ok && data.status === 'success') {
        const routeCartesians = data.path.map(p => Cartesian3.fromDegrees(p.lng, p.lat));
        setRoutePath(routeCartesians);
      } else {
        setRouteError(data.error || "Failed to calculate route");
      }
    } catch (error) {
      console.error("Routing failed:", error);
      setRouteError("Error connecting to routing service");
    } finally {
      setCalculatingRoute(false);
    }
  };

  // Legend Data for RescueNet Classes
  const legendItems = [
    { label: 'Water (Natural/Flood)', color: '#1E90FF' },
    { label: 'Building - No Damage', color: '#32CD32' },
    { label: 'Building - Minor Damage', color: '#FFD700' },
    { label: 'Building - Major Damage', color: '#FF8C00' },
    { label: 'Building - Total Destruction', color: '#8B0000' },
    { label: 'Vehicle', color: '#8A2BE2' },
    { label: 'Road - Clear', color: '#A9A9A9' },
    { label: 'Road - Blocked', color: '#FF0000' },
    { label: 'Tree', color: '#228B22' },
    { label: 'Pool', color: '#00BFFF' },
    { label: 'Other', color: '#808080' }
  ];

  return (
    <div style={{ display: 'flex', height: "100vh", width: "100vw", backgroundColor: "#1e1e1e", color: "white", overflow: 'hidden' }}>
      
      <LeftSidebar
        liveSurvivors={liveSurvivors}
        onRouteRequest={handleRouteRequest}
        calculatingRoute={calculatingRoute}
        routeError={routeError}
      />

      <div style={{ flexGrow: 1, position: 'relative' }}>
        {/* Top Overlay HUD */}
        <div style={{ position: 'absolute', top: 15, left: 15, zIndex: 10, background: 'rgba(0,0,0,0.8)', padding: '10px 20px', borderRadius: '8px', border: '1px solid #333' }}>
          <h1 style={{ margin: 0, fontSize: '1.5rem', color: '#00ffcc' }}>Project Vayu Drishti</h1>
          <p style={{ margin: '5px 0 0 0', fontSize: '0.9rem', color: '#ccc' }}>
            Historical Events: {disasterEvents.length} <br/>
            Live Survivors Found: {liveSurvivors.length} <br/>
            Damage Zones Mapped: {liveDamage.length}
          </p>
        </div>

        {/* Map Legend Overlay */}
        <div style={{ position: 'absolute', bottom: 35, right: 15, zIndex: 10, background: 'rgba(0,0,0,0.85)', padding: '10px', borderRadius: '8px', border: '1px solid #333', fontSize: '0.75rem', fontFamily: 'sans-serif' }}>
          <h4 style={{ margin: '0 0 8px 0', color: '#ddd', fontSize: '0.85rem', borderBottom: '1px solid #555', paddingBottom: '4px' }}>Segmentation Legend</h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
            {legendItems.map((item, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <div style={{ width: '12px', height: '12px', backgroundColor: item.color, borderRadius: '2px', border: '1px solid #000' }}></div>
                <span style={{ color: '#ccc' }}>{item.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Cesium 3D Globe */}
        <Viewer 
          full 
          animation={false} 
          timeline={false} 
          ref={viewerRef}
          onMouseDown={() => setIsTracked(false)}
          // --- ADD THESE TWO LINES TO BYPASS BING MAPS ---
          baseLayerPicker={false} 
          imageryProvider={false}
        >

          {/* 2. ADD THIS: Explicitly mount the Esri World Imagery Satellite Map */}
          {esriProvider && <ImageryLayer imageryProvider={esriProvider} />}
          {/* 1. The Drone Entity */}
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

          {/* 2. Initial Database Load (Historical) */}
          {disasterEvents.map((event, index) => {
            if(!event?.geometry?.coordinates) return null;
            const [lng, lat] = event.geometry.coordinates;
            return (
              <Entity
                key={`db-${index}`}
                position={Cartesian3.fromDegrees(lng, lat)}
                point={{ pixelSize: 8, color: Color.YELLOW }}
                name={`Event ID: ${index}`}
              />
            );
          })}

          {/* --- 3. LIVE SURVIVORS (From YOLO) --- */}
          {liveSurvivors.map((survivor, index) => (
            <Entity
              key={`live-surv-${index}`}
              position={Cartesian3.fromDegrees(survivor.lng, survivor.lat)}
              point={{ 
                pixelSize: 12, 
                color: Cesium.Color.fromCssColorString(survivor.color),
                outlineColor: Color.WHITE,
                outlineWidth: 2
              }}
              name={`Survivors Detected: ${survivor.count}`}
            />
          ))}

          {/* --- 4. LIVE DAMAGE ZONES (From YOLO-seg) --- */}
          {liveDamage.map((damage, index) => {
            // Draw a bounded box of roughly 20x20 meters around the detection coordinate
            const offset = 0.00015; 
            return (
              <Entity
                key={`live-dmg-${index}`}
                name={`${damage.label} Zone`}
                rectangle={{
                  coordinates: Cesium.Rectangle.fromDegrees(
                    damage.lng - offset, // West
                    damage.lat - offset, // South
                    damage.lng + offset, // East
                    damage.lat + offset  // North
                  ),
                  material: Cesium.Color.fromCssColorString(damage.color).withAlpha(1.0),
                  // height: 0, // Clamps the rectangle to the ground level
                  outline: true,
                  outlineColor: Cesium.Color.fromCssColorString(damage.color)
                }}
              />
            );
          })}

          {/* --- 5. SAFE ROUTE POLYLINE --- */}
          {routePath.length > 0 && (
            <Entity
              name="Safe Route"
              polyline={{
                positions: routePath,
                width: 5,
                material: new Cesium.PolylineGlowMaterialProperty({
                  glowPower: 0.2,
                  color: Cesium.Color.CYAN
                })
              }}
            />
          )}

          {/* --- 6. RESCUE BASE STATION --- */}
          <Entity
            position={Cartesian3.fromDegrees(78.4850, 17.3840)}
            point={{ pixelSize: 15, color: Color.BLUE, outlineColor: Color.WHITE, outlineWidth: 2 }}
            label={{
              text: "Rescue Base",
              font: "14px monospace",
              fillColor: Color.WHITE,
              verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
              pixelOffset: new Cesium.Cartesian2(0, -20)
            }}
          />
        </Viewer>
      </div>

      <RightSidebar 
        telemetry={telemetry} 
        onTrack={() => setIsTracked(true)} 
        isTracked={isTracked} 
      />
    </div>
  );
}

export default App;