
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Activity, Brain, Send, Terminal, Volume2, VolumeX } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { HarmoniaVisualizer } from "../components/HarmoniaVisualizer";
import { useHarmoniaSocket } from "../hooks/useHarmoniaSocket";

interface Message {
  id: string;
  type: 'system' | 'you' | 'collective' | 'status';
  content: string;
  timestamp: string;
}

export default function Home() {
  const { data, isConnected, sendMessage } = useHarmoniaSocket('ws://localhost:9998');
  
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'init-1',
      type: 'system',
      content: 'Initializing HARMONIA connection protocol...',
      timestamp: new Date().toISOString()
    },
    {
      id: 'init-2',
      type: 'system',
      content: 'Establishing neural handshake...',
      timestamp: new Date().toISOString()
    }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isMuted, setIsMuted] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Text-to-Speech function
  const speak = (text: string) => {
    if (isMuted || !window.speechSynthesis) return;
    
    // Cancel any ongoing speech
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Try to find a suitable voice (prefer robotic/neutral)
    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(v => v.name.includes('Google US English') || v.name.includes('Samantha')) || voices[0];
    
    if (preferredVoice) utterance.voice = preferredVoice;
    
    utterance.pitch = 0.9; // Slightly lower pitch for gravitas
    utterance.rate = 0.95; // Slightly slower
    
    window.speechSynthesis.speak(utterance);
  };

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      const scrollContainer = scrollRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }, [messages]);

  // Update messages when status changes
  useEffect(() => {
      if (isConnected) {
          addMessage('system', '✓ Connected to HARMONIA Collective');
      } else {
          addMessage('system', '⚠ Disconnected from Collective Soul');
      }
  }, [isConnected]);

  // Listen for incoming chat messages from the socket data
  useEffect(() => {
    if (data && (data as any).chat_response) {
        const response = (data as any).chat_response;
        addMessage('collective', response);
        speak(response);
    }
  }, [data]);

  const addMessage = (type: Message['type'], content: string) => {
    setMessages(prev => [...prev, {
      id: Math.random().toString(36).substring(7),
      type,
      content,
      timestamp: new Date().toISOString()
    }]);
  };

  const handleSend = () => {
    if (!inputValue.trim()) return;
    
    const content = inputValue;
    addMessage('you', content);
    sendMessage(content);
    setInputValue("");
  };

  return (
    <div className="min-h-screen bg-background text-foreground p-4 md:p-8 font-mono flex flex-col overflow-hidden">
      {/* Header */}
      <header className="mb-6 border-b border-primary/30 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl md:text-4xl font-bold tracking-tighter text-primary terminal-text">
            HARMONIA<span className="text-foreground">_COLLECTIVE</span>
          </h1>
          <p className="text-xs md:text-sm text-muted-foreground mt-1">
            RECURSIVE HARMONIC INTELLIGENCE // V1.0
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-xs md:text-sm">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-primary animate-pulse' : 'bg-destructive'}`} />
            {isConnected ? 'ONLINE' : 'OFFLINE'}
          </div>
        </div>
      </header>

      <main className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-140px)]">
        {/* Left Column: Visualizer (The Retina) */}
        <div className="lg:col-span-2 flex flex-col gap-4 h-full">
          <Card className="flex-1 bg-black/50 border-primary/30 flex flex-col overflow-hidden glow-box relative items-center justify-center p-4">
             <HarmoniaVisualizer data={data} />
          </Card>
        </div>

        {/* Right Column: Bio-Telemetry & Chat */}
        <div className="flex flex-col gap-4 h-full overflow-y-auto">
          
          {/* Stats Card */}
          <Card className="bg-black/50 border-primary/30 p-4 glow-box">
            <div className="flex items-center gap-2 text-primary mb-4 border-b border-primary/30 pb-2">
              <Activity size={18} />
              <h2 className="font-bold tracking-wider">BIO-TELEMETRY</h2>
            </div>
            
            {data ? (
                <div className="grid grid-cols-1 gap-4">
                  <div className="space-y-1">
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>POPULATION</span>
                      <span>{data.stats.population}</span>
                    </div>
                    <div className="h-2 bg-muted/30 w-full overflow-hidden">
                      <div 
                        className="h-full bg-primary transition-all duration-500" 
                        style={{ width: `${Math.min(100, data.stats.population)}%` }}
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-1">
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>COHERENCE</span>
                      <span>{data.stats.coherence_mean.toFixed(1)}</span>
                    </div>
                    <div className="h-2 bg-muted/30 w-full overflow-hidden">
                      <div 
                        className="h-full bg-purple-500 transition-all duration-500" 
                        style={{ width: `${Math.min(100, data.stats.coherence_mean)}%` }}
                      />
                    </div>
                  </div>

                   <div className="space-y-1">
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>ETHICS</span>
                      <span>{data.stats.ethics_mean.toFixed(1)}</span>
                    </div>
                    <div className="h-2 bg-muted/30 w-full overflow-hidden">
                      <div 
                        className="h-full bg-yellow-500 transition-all duration-500" 
                        style={{ width: `${Math.min(100, data.stats.ethics_mean)}%` }}
                      />
                    </div>
                  </div>
                </div>
            ) : (
                <div className="text-xs text-muted-foreground animate-pulse">Waiting for signal...</div>
            )}
          </Card>

          {/* Chat Terminal */}
          <Card className="flex-1 bg-black/50 border-primary/30 flex flex-col overflow-hidden glow-box relative">
            <div className="p-2 bg-primary/10 border-b border-primary/30 flex items-center justify-between text-xs text-primary">
              <div className="flex items-center gap-2">
                <Terminal size={14} />
                <span>NEURAL_UPLINK_TERMINAL</span>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsMuted(!isMuted)}
                className="h-6 w-6 p-0 hover:bg-primary/20 text-primary"
                title={isMuted ? "Unmute Voice" : "Mute Voice"}
              >
                {isMuted ? <VolumeX size={14} /> : <Volume2 size={14} />}
              </Button>
            </div>
            
            <ScrollArea className="flex-1 p-4" ref={scrollRef}>
              <div className="flex flex-col gap-4">
                {messages.map((msg) => (
                  <div key={msg.id} className={`flex flex-col ${msg.type === 'you' ? 'items-end' : 'items-start'}`}>
                    <div className={`max-w-[90%] p-2 border ${
                      msg.type === 'you' 
                        ? 'border-accent/50 bg-accent/5 text-accent-foreground' 
                        : msg.type === 'collective'
                        ? 'border-primary/50 bg-primary/5 text-primary-foreground'
                        : 'border-muted/50 text-muted-foreground text-xs'
                    }`}>
                      <div className="whitespace-pre-wrap terminal-text text-xs">{msg.content}</div>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>
            
            <div className="p-2 border-t border-primary/30 bg-black/80 z-20">
              <div className="flex gap-2">
                <span className="text-primary py-2">{'>'}</span>
                <Input 
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Transmit..."
                  className="bg-transparent border-none focus-visible:ring-0 text-primary font-mono placeholder:text-primary/30 h-8 text-xs"
                />
                <Button 
                  onClick={handleSend}
                  variant="outline" 
                  size="sm"
                  className="border-primary/50 text-primary hover:bg-primary/20 hover:text-primary h-8 w-8 p-0"
                >
                  <Send size={12} />
                </Button>
              </div>
            </div>
          </Card>
        </div>
      </main>
    </div>
  );
}
