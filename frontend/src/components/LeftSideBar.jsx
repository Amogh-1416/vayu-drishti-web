import React from 'react';

const LeftSidebar = () => {
  return (
    <div style={{
      width: '250px',
      height: '100vh',
      backgroundColor: '#1a1a1a',
      color: 'white',
      padding: '20px',
      borderRight: '1px solid #333',
      fontFamily: 'sans-serif'
    }}>
      <h2 style={{ fontSize: '1.2rem', marginBottom: '20px' }}>Filters</h2>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
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
  );
};

export default LeftSidebar;