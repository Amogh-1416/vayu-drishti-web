const labelColors = {
  FIRE: '#FF4500',
  POOL: '#1FFFF',
  COLLAPSE: '#8B4513',
  ROAD: '#FFFF00',
  OTHER: '#808080',
  TREE: '#32BA81',
  DEBRIS: '#12A8AB',
  BUILDING_MAJOR_DAMAGE: '#1E90FF',
  BUILDING_MEDIUM_DAMAGE: '#58AD45',
  BUILDING_TOTAL_DAMAGE: '#88AD45'
};

function Color() {
  return (
    <div>
      {Object.entries(labelColors).map(([label, color]) => (
        <div key={label}>
          <span style={{ color }}>{label}</span>
        </div>
      ))}
    </div>
  );
}

export default Color;