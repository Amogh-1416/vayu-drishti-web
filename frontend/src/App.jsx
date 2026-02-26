import React, { useMemo } from 'react';
import { Viewer, Entity } from "resium";
import * as Cesium from "cesium"; // Fixes: "Cesium is not defined"
import { Cartesian3, HermitePolynomialApproximation } from "cesium";
import useWebSocket from './hooks/useWebSocket';

function App() {
  // Use explicit IP to match your backend logs
  const telemetry = useWebSocket('ws://127.0.0.1:8000/ws/telemetry/');

  const dronePosition = useMemo(() => {
    if (telemetry?.latitude && telemetry?.longitude) {
      return Cartesian3.fromDegrees(telemetry.longitude, telemetry.latitude, telemetry.altitude || 100);
    }
    return Cartesian3.fromDegrees(78.4867, 17.3850, 100); 
  }, [telemetry]);

  return (
    <Viewer full>
      <Entity
        position={dronePosition}
        point={{ pixelSize: 20, color: Cesium.Color.RED }}
        tracked={true}
        // Smooths out the 1-second updates into a glide
        interpolationAlgorithm={HermitePolynomialApproximation}
        interpolationDegree={2}
      />
    </Viewer>
  );
}

export default App;