
import { useEffect, useState, useRef } from 'react';

export interface EntityState {
  id: string;
  psi: number;      // Awareness/Energy
  phi: number;      // Stability
  ethics: number;   // Alignment
  age: number;
  generation: number;
  energy: number;
  knowledge: number;
  maturity: number;
  coherence: number;
  self_awareness: number;
}

export interface CollectiveState {
  timestamp: string;
  stats: {
    population: number;
    coherence_mean: number;
    ethics_mean: number;
    self_awareness_mean: number;
    status: string; // RESONANT, ENTROPIC, etc.
  };
  entities: EntityState[];
}

export function useHarmoniaSocket(url: string = 'ws://localhost:10010') {
  const [data, setData] = useState<CollectiveState | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const connect = () => {
      console.log('Connecting to Harmonia Soul...', url);
      const socket = new WebSocket(url);
      socketRef.current = socket;

      socket.onopen = () => {
        console.log('Connected to Collective Soul.');
        setIsConnected(true);
      };

      socket.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          // The server sends { type: 'audio_frame', data: ... } for audio
          // We need to filter for the full state updates if they are mixed,
          // OR we need to update the server to send full state JSON for the visualizer.
          // Assuming the server broadcasts the full state JSON periodically.
          if (parsed.stats) {
             setData(parsed);
          }
        } catch (e) {
          console.error('Failed to parse soul packet:', e);
        }
      };

      socket.onclose = () => {
        console.log('Disconnected from Collective Soul.');
        setIsConnected(false);
        // Reconnect logic could go here
        setTimeout(connect, 3000);
      };
    };

    connect();

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [url]);

  const sendMessage = (text: string) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type: 'chat', content: text }));
    }
  };

  return { data, isConnected, sendMessage };
}
