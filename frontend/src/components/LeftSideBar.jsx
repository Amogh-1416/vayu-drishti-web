import React from 'react';

const LeftSidebar = ({ liveSurvivors, onRouteRequest, calculatingRoute, routeError }) => {
  return (
    <div style={{
      width: '250px',
      height: '100vh',
      backgroundColor: '#1a1a1a',
      color: 'white',
      padding: '20px',
      borderRight: '1px solid #333',
      fontFamily: 'sans-serif',
      display: 'flex',
      flexDirection: 'column',
      gap: '20px',
      overflowY: 'auto'
    }}>
      <div>
        <h2 style={{ fontSize: '1.2rem', marginBottom: '15px' }}>Filters</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <label style={{ fontSize: '0.9rem' }}>
            <input type="checkbox" defaultChecked /> Survivor Clusters
          </label>
          <label style={{ fontSize: '0.9rem' }}>
            <input type="checkbox" defaultChecked /> Damage Reports
          </label>
          <label style={{ fontSize: '0.9rem' }}>
            <input type="checkbox" defaultChecked /> Active Drones
          </label>
        </div>
      </div>

      <div style={{ borderTop: '1px solid #333', paddingTop: '20px' }}>
        <h2 style={{ fontSize: '1.2rem', marginBottom: '15px', color: '#ff4d4d' }}>Emergency Routing</h2>
        {routeError && (
            <div style={{ color: '#ff4d4d', fontSize: '0.8rem', marginBottom: '10px' }}>
              Error: {routeError}
            </div>
        )}
        <p style={{ fontSize: '0.8rem', color: '#ccc', marginBottom: '15px' }}>
          Select a detected survivor cluster to calculate a safe route from Rescue Base.
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {liveSurvivors && liveSurvivors.length === 0 ? (
            <p style={{ fontSize: '0.8rem', color: '#888' }}>No survivors detected yet...</p>
          ) : (
            liveSurvivors.map((survivor, index) => (
              <div
                key={index}
                style={{
                  background: '#2a2a2a',
                  padding: '10px',
                  borderRadius: '5px',
                  border: '1px solid #444'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '5px' }}>
                  <span style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>Cluster #{index + 1}</span>
                  <span style={{ fontSize: '0.8rem', color: '#00ffcc' }}>{survivor.count} pax</span>
                </div>
                <button
                  onClick={() => onRouteRequest(survivor)}
                  disabled={calculatingRoute}
                  style={{
                    width: '100%',
                    padding: '8px',
                    backgroundColor: calculatingRoute ? '#555' : '#007bff',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: calculatingRoute ? 'not-allowed' : 'pointer',
                    fontSize: '0.8rem',
                    fontWeight: 'bold',
                    transition: 'background-color 0.2s'
                  }}
                >
                  {calculatingRoute ? 'Calculating...' : 'Calculate Safe Route'}
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default LeftSidebar;