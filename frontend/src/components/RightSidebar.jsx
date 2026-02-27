import React from 'react';

const RightSidebar = ({ telemetry, onTrack, isTracked }) => {
  return (
    <div style={{
      width: '300px',
      height: '100vh',
      backgroundColor: '#1e1e1e',
      color: 'white',
      padding: '20px',
      borderLeft: '1px solid #333',
      display: 'flex',
      flexDirection: 'column',
      fontFamily: 'monospace'
    }}>
      <h2 style={{ 
        fontSize: '1.2rem', 
        marginBottom: '20px', 
        borderBottom: '1px solid #444', 
        paddingBottom: '10px' 
      }}>
        Fleet Manager
      </h2>

      {/* DRONE STATUS CARD */}
      <div 
        onClick={onTrack}
        style={{ 
          background: isTracked ? '#1a331a' : '#2a2a2a', 
          padding: '15px', 
          borderRadius: '8px', 
          marginBottom: '20px', 
          border: isTracked ? '1px solid #00ffcc' : '1px solid #444',
          cursor: 'pointer',
          transition: 'all 0.3s ease'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
          <h3 style={{ margin: 0, fontSize: '1rem' }}>Alpha-1</h3>
          <span style={{ 
            fontSize: '0.7rem', 
            color: isTracked ? '#00ffcc' : '#888' 
          }}>
            {isTracked ? '● TRACKING' : '○ IDLE'}
          </span>
        </div>
        
        {/* LIVE DATA UPDATES */}
        <p style={{ margin: '5px 0', fontSize: '0.8rem', color: '#00ffcc' }}>
          STATUS: {telemetry ? 'IN-FLIGHT' : 'SEARCHING...'}
        </p>
        <div style={{ fontSize: '0.75rem', color: '#aaa' }}>
          <p style={{ margin: '2px 0' }}>LAT: {telemetry?.latitude?.toFixed(5) || "0.00000"}</p>
          <p style={{ margin: '2px 0' }}>LON: {telemetry?.longitude?.toFixed(5) || "0.00000"}</p>
        </div>
      </div>

      {/* LIVE CAMERA FEED OVERLAY */}
      <div style={{ 
        width: '100%', 
        height: '180px', 
        background: '#000', 
        display: 'flex', 
        flexDirection: 'column',
        alignItems: 'center', 
        justifyContent: 'center', 
        borderRadius: '8px', 
        border: '1px solid #444',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {telemetry ? (
          <div style={{ textAlign: 'center', color: '#00ffcc', zIndex: 1 }}>
            <p style={{ fontSize: '0.7rem', margin: '0 0 5px 0', color: '#555' }}>LIVE PERSPECTIVE</p>
            <p style={{ fontSize: '1.2rem', margin: 0 }}>ALT: {telemetry?.altitude?.toFixed(1)}m</p>
            <p style={{ fontSize: '0.6rem', color: 'red', marginTop: '10px' }}>[ ENCRYPTED STREAM ]</p>
          </div>
        ) : (
          <p style={{ color: '#555', margin: 0, fontSize: '0.9rem' }}>[ Camera Feed Offline ]</p>
        )}
        
        {/* Subtle Scanline Effect */}
        <div style={{ 
          position: 'absolute', top: 0, left: 0, width: '100%', height: '100%',
          background: 'linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06))',
          zIndex: 2, backgroundSize: '100% 2px, 3px 100%', pointerEvents: 'none'
        }}></div>
      </div>
    </div>
  );
};

export default RightSidebar;