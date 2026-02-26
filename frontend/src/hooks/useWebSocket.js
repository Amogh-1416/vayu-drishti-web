import { useEffect, useRef } from 'react';

const useWebSocket = (url, onMessage) => {
  const socketRef = useRef(null);

  useEffect(() => {
    socketRef.current = new WebSocket(url);

    socketRef.current.onopen = () => {
      console.log('✅ Connected to WebSocket Stream');
    };

    // Requirement: Connect and simply print incoming live drone coordinates
    socketRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('🛰️ Live Telemetry Data:', data);
        if (typeof onMessage === 'function') onMessage(data);
      } catch (err) {
        console.error('❌ Error parsing message:', err);
      }
    };

    socketRef.current.onclose = () => console.log('🔌 Connection Closed');

    return () => {
      if (socketRef.current) socketRef.current.close();
    };
  }, [url, onMessage]);

  return socketRef.current;
};

export default useWebSocket;