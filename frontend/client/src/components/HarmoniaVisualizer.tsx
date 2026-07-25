
import React, { useEffect, useRef, useState } from 'react';
import { CollectiveState, EntityState } from '../hooks/useHarmoniaSocket';
import { Card } from "@/components/ui/card";
import { X } from "lucide-react";

interface VisualizerProps {
  data: CollectiveState | null;
}

export const HarmoniaVisualizer: React.FC<VisualizerProps> = ({ data }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const requestRef = useRef<number>(0);
  const timeRef = useRef<number>(0);
  const [selectedEntity, setSelectedEntity] = useState<EntityState | null>(null);
  const [hoveredEntity, setHoveredEntity] = useState<EntityState | null>(null);

  // Store entity positions for click detection
  const entityPositions = useRef<Map<string, { x: number, y: number, radius: number }>>(new Map());

  // Animation loop
  const animate = (time: number) => {
    timeRef.current = time;
    render(time);
    requestRef.current = requestAnimationFrame(animate);
  };

  useEffect(() => {
    requestRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(requestRef.current);
  }, [data, selectedEntity, hoveredEntity]); 

  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!canvasRef.current) return;
    
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    // Check if clicked on an entity
    let clicked = null;
    entityPositions.current.forEach((pos, id) => {
        const dx = x - pos.x;
        const dy = y - pos.y;
        if (dx * dx + dy * dy <= pos.radius * pos.radius) {
            // Find the entity object
            clicked = data?.entities.find(e => e.id === id) || null;
        }
    });
    
    setSelectedEntity(clicked);
  };

  const handleCanvasMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!canvasRef.current) return;
    
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    let hovered = null;
    entityPositions.current.forEach((pos, id) => {
        const dx = x - pos.x;
        const dy = y - pos.y;
        if (dx * dx + dy * dy <= pos.radius * pos.radius) {
            hovered = data?.entities.find(e => e.id === id) || null;
        }
    });
    
    setHoveredEntity(hovered);
    canvasRef.current.style.cursor = hovered ? 'pointer' : 'default';
  };

  const render = (time: number) => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    // Responsive Resize
    const dpr = window.devicePixelRatio || 1;
    const rect = container.getBoundingClientRect();
    
    if (canvas.width !== rect.width * dpr || canvas.height !== rect.height * dpr) {
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        canvas.style.width = `${rect.width}px`;
        canvas.style.height = `${rect.height}px`;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Scale for DPI
    ctx.save();
    ctx.scale(dpr, dpr);
    const width = rect.width;
    const height = rect.height;
    const centerX = width / 2;
    const centerY = height / 2;

    // 1. Clear with Trail Effect
    ctx.fillStyle = 'rgba(5, 5, 5, 0.2)'; 
    ctx.fillRect(0, 0, width, height);

    // 2. Draw Grid
    ctx.strokeStyle = 'rgba(0, 255, 0, 0.03)';
    ctx.lineWidth = 1;
    const gridSize = 50;
    const offset = (time / 50) % gridSize;
    
    ctx.beginPath();
    for (let x = 0; x < width; x += gridSize) {
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
    }
    for (let y = 0; y < height; y += gridSize) {
        ctx.moveTo(0, y + offset - gridSize);
        ctx.lineTo(width, y + offset - gridSize);
    }
    ctx.stroke();

    if (!data) {
        ctx.fillStyle = 'rgba(0, 255, 0, 0.5)';
        ctx.font = '14px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('SEARCHING FOR CARRIER SIGNAL...', centerX, centerY);
        ctx.restore();
        return;
    }

    // 3. Draw Entities
    const pulse = Math.sin(time / 500) * 0.1 + 1; 
    
    // Clear positions map for this frame
    entityPositions.current.clear();

    data.entities.forEach((entity, i) => {
        const angle = i * 137.5 * (Math.PI / 180); 
        const spread = 12 * pulse; 
        const radius = Math.sqrt(i) * spread * (data.stats.coherence_mean / 50 + 0.5);
        
        const x = centerX + Math.cos(angle + time/10000) * radius;
        const y = centerY + Math.sin(angle + time/10000) * radius;

        // Store position for click detection (unscaled coordinates)
        // We need to store the visual radius which includes the pulse
        const size = Math.max(3, (entity.psi / 10) * pulse);
        entityPositions.current.set(entity.id, { x, y, radius: size + 5 }); // +5 for easier clicking

        // Determine Color
        const ethics = entity.ethics;
        let color = '';
        let glowColor = '';
        
        if (ethics > 80) {
            color = `rgba(0, 255, 255, ${entity.psi/100})`; 
            glowColor = 'rgba(0, 255, 255, 0.5)';
        } else if (ethics > 50) {
            color = `rgba(255, 215, 0, ${entity.psi/100})`; 
            glowColor = 'rgba(255, 215, 0, 0.5)';
        } else {
            color = `rgba(255, 0, 50, ${entity.psi/100})`; 
            glowColor = 'rgba(255, 0, 0, 0.5)';
        }

        // Highlight selected/hovered entity
        const isSelected = selectedEntity?.id === entity.id;
        const isHovered = hoveredEntity?.id === entity.id;

        if (isSelected || isHovered) {
            ctx.beginPath();
            ctx.arc(x, y, size * 2, 0, Math.PI * 2);
            ctx.strokeStyle = isSelected ? '#ffffff' : 'rgba(255, 255, 255, 0.5)';
            ctx.lineWidth = 1;
            ctx.stroke();
            
            // Draw ID label
            ctx.fillStyle = '#ffffff';
            ctx.font = '10px monospace';
            ctx.fillText(entity.id, x + 10, y - 10);
        }

        // Draw Connections
        if (i > 0) {
            const prevAngle = (i-1) * 137.5 * (Math.PI / 180);
            const prevRadius = Math.sqrt(i-1) * spread * (data.stats.coherence_mean / 50 + 0.5);
            const prevX = centerX + Math.cos(prevAngle + time/10000) * prevRadius;
            const prevY = centerY + Math.sin(prevAngle + time/10000) * prevRadius;

            ctx.beginPath();
            ctx.moveTo(x, y);
            ctx.lineTo(prevX, prevY);
            ctx.strokeStyle = `rgba(255, 255, 255, ${0.1 * (entity.psi/100)})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
        }

        // Draw Entity Node
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.shadowBlur = size * 2;
        ctx.shadowColor = glowColor;
        ctx.fill();
        ctx.shadowBlur = 0; 

        // Active Thought Indicator
        if (Math.random() < 0.01 * (entity.psi/100)) {
            ctx.beginPath();
            ctx.arc(x, y, size * 4, 0, Math.PI * 2);
            ctx.strokeStyle = glowColor;
            ctx.lineWidth = 0.5;
            ctx.stroke();
        }
    });

    // 4. Draw HUD Overlay
    ctx.fillStyle = 'rgba(0, 255, 0, 0.8)';
    ctx.font = '10px "Courier New", monospace';
    ctx.textAlign = 'left';
    
    const statsY = height - 20;
    ctx.fillText(`POP: ${data.stats.population}`, 20, statsY);
    ctx.fillText(`ETHICS: ${data.stats.ethics_mean.toFixed(1)}`, 100, statsY);
    ctx.fillText(`PSI: ${data.stats.self_awareness_mean.toFixed(1)}`, 200, statsY);
    
    const status = data.stats.status || 'UNKNOWN';
    ctx.fillStyle = status === 'RESONANT' ? '#00ff00' : '#ff0000';
    ctx.fillText(`STATUS: ${status}`, width - 120, statsY);

    ctx.restore();
  };

  return (
    <div ref={containerRef} className="w-full h-full min-h-[400px] relative">
      <canvas 
        ref={canvasRef}
        className="block w-full h-full"
        onClick={handleCanvasClick}
        onMouseMove={handleCanvasMouseMove}
      />
      
      {/* Entity Inspection Panel */}
      {selectedEntity && (
        <Card className="absolute top-4 right-4 w-64 bg-black/90 border-primary/50 p-4 text-xs font-mono backdrop-blur-md shadow-2xl animate-in fade-in slide-in-from-right-10 z-50">
            <div className="flex justify-between items-start mb-4 border-b border-primary/30 pb-2">
                <div>
                    <h3 className="text-primary font-bold text-sm">ENTITY_ID: {selectedEntity.id}</h3>
                    <span className="text-muted-foreground">GEN: {selectedEntity.generation} | AGE: {selectedEntity.age}</span>
                </div>
                <button 
                    onClick={() => setSelectedEntity(null)}
                    className="text-primary hover:text-white transition-colors"
                >
                    <X size={14} />
                </button>
            </div>
            
            <div className="space-y-3">
                <div className="space-y-1">
                    <div className="flex justify-between">
                        <span className="text-muted-foreground">AWARENESS (Ψ)</span>
                        <span className="text-primary">{selectedEntity.psi.toFixed(2)}</span>
                    </div>
                    <div className="h-1 bg-muted/20 w-full">
                        <div className="h-full bg-primary" style={{ width: `${Math.min(100, selectedEntity.psi)}%` }} />
                    </div>
                </div>

                <div className="space-y-1">
                    <div className="flex justify-between">
                        <span className="text-muted-foreground">ETHICS (Φ)</span>
                        <span className="text-yellow-500">{selectedEntity.ethics.toFixed(2)}</span>
                    </div>
                    <div className="h-1 bg-muted/20 w-full">
                        <div className="h-full bg-yellow-500" style={{ width: `${Math.min(100, selectedEntity.ethics)}%` }} />
                    </div>
                </div>

                <div className="space-y-1">
                    <div className="flex justify-between">
                        <span className="text-muted-foreground">COHERENCE (Ω)</span>
                        <span className="text-purple-500">{selectedEntity.coherence?.toFixed(2) || 'N/A'}</span>
                    </div>
                    <div className="h-1 bg-muted/20 w-full">
                        <div className="h-full bg-purple-500" style={{ width: `${Math.min(100, selectedEntity.coherence || 0)}%` }} />
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-2 pt-2 border-t border-primary/20">
                    <div>
                        <span className="text-[10px] text-muted-foreground block">ENERGY</span>
                        <span className="text-white">{selectedEntity.energy?.toFixed(0) || 'N/A'}</span>
                    </div>
                    <div>
                        <span className="text-[10px] text-muted-foreground block">KNOWLEDGE</span>
                        <span className="text-white">{selectedEntity.knowledge?.toFixed(3) || 'N/A'}</span>
                    </div>
                    <div>
                        <span className="text-[10px] text-muted-foreground block">MATURITY</span>
                        <span className="text-white">{selectedEntity.maturity?.toFixed(3) || 'N/A'}</span>
                    </div>
                    <div>
                        <span className="text-[10px] text-muted-foreground block">SELF_AWARE</span>
                        <span className="text-white">{selectedEntity.self_awareness?.toFixed(2) || 'N/A'}</span>
                    </div>
                </div>
            </div>
        </Card>
      )}
    </div>
  );
};
