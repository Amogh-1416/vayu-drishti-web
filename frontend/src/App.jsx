import React, { useMemo, useRef, useState } from 'react';
import { Viewer, Entity } from "resium";
import * as Cesium from "cesium";
import { Cartesian3, HermitePolynomialApproximation } from "cesium";
import useWebSocket from './hooks/useWebSocket';

function App() {
  const viewerRef = useRef(null);
  const [isTracked, setIsTracked] = useState(false);

  // 1. WebSocket connection using 127.0.0.1 for local stability on macOS
  const telemetry = useWebSocket('ws://127.0.0.1:8000/ws/telemetry/');

  // 2. Compute smooth drone position using Hermite Interpolation
  const dronePosition = useMemo(() => {
    if (telemetry?.latitude && telemetry?.longitude) {
      return Cartesian3.fromDegrees(
        telemetry.longitude, 
        telemetry.latitude, 
        telemetry.altitude || 60
      );
    }
    // Default fallback to starting coordinates in Hyderabad
    return Cartesian3.fromDegrees(78.4867, 17.3850, 60); 
  }, [telemetry]);

  
  const handleDroneClick = () => {
  if (viewerRef.current && viewerRef.current.cesiumElement && telemetry) {
    const viewer = viewerRef.current.cesiumElement;
    const targetPos = Cartesian3.fromDegrees(telemetry.longitude, telemetry.latitude, 150);

    if (isTracked) {
      viewer.camera.setView({
        destination: targetPos
      });
    } else {
      viewer.camera.flyTo({
        destination: targetPos,
        duration: 1.0 
      });
      setIsTracked(true);
    }
  }
};

  return (
    <div style={{ position: 'relative', width: '100%', height: '100vh', overflow: 'hidden', background: '#000' }}>
      
      {/* CESIUM VIEWER */}
      <Viewer 
        full 
        ref={viewerRef} 
        timeline={false} 
        animation={false}
        // Unlock camera if user clicks on the map
        onMouseDown={() => setIsTracked(false)} 
      >
        <Entity
          name="Alpha-1"
          position={dronePosition}
          point={{ pixelSize: 20, color: Cesium.Color.RED }}
          label={{ 
            text: "Alpha-1", 
            font: "14px monospace", 
            fillColor: Cesium.Color.LIME,
            outlineColor: Cesium.Color.BLACK,
            outlineWidth: 2,
            verticalOrigin: Cesium.VerticalOrigin.BOTTOM, 
            pixelOffset: new Cesium.Cartesian2(0, -20) 
          }}
          tracked={isTracked} // Controls if camera follows the drone
          interpolationAlgorithm={HermitePolynomialApproximation}
          interpolationDegree={2}
        />
      </Viewer>

      {/* RIGHT SIDEBAR: FLEET MANAGER UI (Issue #31) */}
      <div style={{
        position: 'absolute', right: 0, top: 0, width: '280px', height: '100%',
        backgroundColor: 'rgba(15, 15, 15, 0.95)', color: 'white', padding: '20px',
        borderLeft: '1px solid #00ff00', zIndex: 10, fontFamily: 'monospace'
      }}>
        <h2 style={{ color: '#00ff00', borderBottom: '1px solid #333', paddingBottom: '10px' }}>FLEET_MANAGER</h2>
        
        <div 
          onClick={handleDroneClick}
          style={{ 
            cursor: 'pointer', padding: '15px', marginTop: '20px', 
            background: isTracked ? '#1a331a' : '#222', 
            borderRadius: '4px',
            border: isTracked ? '1px solid #00ff00' : '1px solid #444',
            transition: 'all 0.3s ease'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
            <strong style={{ color: '#fff' }}>ALPHA-1</strong>
            <span style={{ color: isTracked ? '#00ff00' : '#888', fontSize: '10px' }}>
              {isTracked ? '● TRACKING' : '○ IDLE'}
            </span>
          </div>
          <p style={{ fontSize: '11px', color: '#00ff00' }}>STATUS: IN-FLIGHT</p>
          <p style={{ fontSize: '10px', color: '#aaa' }}>LAT: {telemetry?.latitude?.toFixed(5) || "---"}</p>
          <p style={{ fontSize: '10px', color: '#aaa' }}>LON: {telemetry?.longitude?.toFixed(5) || "---"}</p>
        </div>
      </div>

      {/* PIP OVERLAY: LIVE TELEMETRY FEED (Issue #31) */}
      {isTracked && (
        <div style={{
          position: 'absolute', bottom: '30px', right: '310px',
          width: '300px', height: '180px', border: '2px solid #00ff00',
          background: '#000', borderRadius: '4px', zIndex: 20, overflow: 'hidden',
          fontFamily: 'monospace'
        }}>
          <div style={{ background: 'rgba(0,255,0,0.2)', color: '#00ff00', padding: '5px', fontSize: '10px', borderBottom: '1px solid #00ff00' }}>
            LIVE_PERSPECTIVE // ALPHA-1
          </div>
          <div style={{ 
            height: 'calc(100% - 25px)', display: 'flex', flexDirection: 'column', 
            justifyContent: 'center', alignItems: 'center', color: '#00ff00',
            textAlign: 'center'
          }}>
            <p style={{ margin: '2px 0' }}>ALTITUDE: {telemetry?.altitude?.toFixed(1)}m</p>
            <p style={{ margin: '2px 0' }}>LAT: {telemetry?.latitude?.toFixed(5)}</p>
            <p style={{ margin: '2px 0' }}>LON: {telemetry?.longitude?.toFixed(5)}</p>
            <p style={{ color: 'red', fontSize: '9px', marginTop: '10px' }}>[ SIMULATED_DATA_STREAM ]</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;