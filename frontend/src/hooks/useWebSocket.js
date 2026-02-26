import { useEffect, useState } from "react";

const useWebSocket = (url) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const socket = new WebSocket(url);

    socket.onmessage = (event) => {
      const parsedData = JSON.parse(event.data);
      setData(parsedData); // Output real-time coordinate state
    };

    return () => socket.close();
  }, [url]);

  return data; 
};

export default useWebSocket;