import { Viewer } from "resium";

function App() {
  return (
    <div style={{ height: "100vh", width: "100vw", margin: 0, padding: 0 }}>
      {/* baseLayerPicker={false} stops it from trying to load locked Ion satellite maps */}
      <Viewer full baseLayerPicker={false} />
    </div>
  );
}

export default App;