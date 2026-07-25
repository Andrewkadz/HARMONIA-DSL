#!/usr/bin/env python3.11
"""
AI System State Inspection API
Provides interface for Φπε operators to inspect AI system state
"""

import threading
import psutil
import torch
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class ThreadInfo:
    """Information about a running thread"""
    id: int
    name: str
    is_alive: bool
    daemon: bool
    
@dataclass
class FileHandleInfo:
    """Information about an open file"""
    path: str
    mode: str
    fd: int
    
@dataclass
class GPUMemoryInfo:
    """Information about GPU memory usage"""
    allocated: float  # GB
    reserved: float   # GB
    free: float       # GB
    total: float      # GB
    utilization: float  # 0-1
    
@dataclass
class OperationInfo:
    """Information about a pending operation"""
    id: str
    type: str
    status: str
    started_at: datetime
    duration: float  # seconds
    
@dataclass
class ConversationMessage:
    """A message in conversation history"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    tokens: int


class AISystemState:
    """
    State Inspection API for AI Systems
    
    This class provides methods for Φπε operators to inspect
    the current state of an AI system.
    
    Used by:
    - Ρ (Perceive) operator - observe state
    - χ (Measure) operator - measure/analyze state
    """
    
    def __init__(self, ai_system=None):
        """
        Initialize state inspector
        
        Args:
            ai_system: The AI system to inspect (e.g., LLM, agent)
        """
        self.ai_system = ai_system
        self._active_threads = []
        self._open_files = []
        self._pending_operations = []
        self._conversation_history = []
        
    # ═══════════════════════════════════════════════════════════════════════
    # THREAD INSPECTION
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_active_threads(self) -> List[ThreadInfo]:
        """
        Get all active threads
        
        Used by: Ρ (Perceive) operator
        
        Returns:
            List of ThreadInfo objects
        """
        threads = []
        for thread in threading.enumerate():
            threads.append(ThreadInfo(
                id=thread.ident,
                name=thread.name,
                is_alive=thread.is_alive(),
                daemon=thread.daemon
            ))
        return threads
    
    def get_thread_count(self) -> int:
        """Get number of active threads"""
        return threading.active_count()
    
    # ═══════════════════════════════════════════════════════════════════════
    # FILE HANDLE INSPECTION
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_open_files(self) -> List[FileHandleInfo]:
        """
        Get all open file handles
        
        Used by: Ρ (Perceive) operator
        
        Returns:
            List of FileHandleInfo objects
        """
        files = []
        process = psutil.Process()
        for file in process.open_files():
            files.append(FileHandleInfo(
                path=file.path,
                mode=file.mode if hasattr(file, 'mode') else 'unknown',
                fd=file.fd
            ))
        return files
    
    def get_file_count(self) -> int:
        """Get number of open files"""
        return len(self.get_open_files())
    
    # ═══════════════════════════════════════════════════════════════════════
    # GPU MEMORY INSPECTION
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_gpu_memory_usage(self) -> Optional[GPUMemoryInfo]:
        """
        Get GPU memory usage
        
        Used by: χ (Measure) operator
        
        Returns:
            GPUMemoryInfo object or None if no GPU
        """
        if not torch.cuda.is_available():
            return None
        
        allocated = torch.cuda.memory_allocated() / 1e9  # GB
        reserved = torch.cuda.memory_reserved() / 1e9    # GB
        
        # Get total GPU memory
        device = torch.cuda.current_device()
        total = torch.cuda.get_device_properties(device).total_memory / 1e9
        free = total - allocated
        utilization = allocated / total if total > 0 else 0
        
        return GPUMemoryInfo(
            allocated=allocated,
            reserved=reserved,
            free=free,
            total=total,
            utilization=utilization
        )
    
    def get_gpu_utilization(self) -> float:
        """Get GPU utilization as 0-1"""
        info = self.get_gpu_memory_usage()
        return info.utilization if info else 0.0
    
    # ═══════════════════════════════════════════════════════════════════════
    # MODEL STATE INSPECTION
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_model_state(self) -> Dict[str, Any]:
        """
        Get current model state
        
        Used by: Ρ (Perceive) operator
        
        Returns:
            Dictionary with model state information
        """
        if self.ai_system is None:
            return {}
        
        state = {
            'model_type': type(self.ai_system).__name__,
            'device': str(self.ai_system.device) if hasattr(self.ai_system, 'device') else 'unknown',
            'parameters': self._count_parameters(),
            'training': self.ai_system.training if hasattr(self.ai_system, 'training') else False,
            'timestamp': datetime.now().isoformat()
        }
        
        return state
    
    def _count_parameters(self) -> int:
        """Count model parameters"""
        if self.ai_system is None:
            return 0
        
        if hasattr(self.ai_system, 'parameters'):
            return sum(p.numel() for p in self.ai_system.parameters())
        return 0
    
    # ═══════════════════════════════════════════════════════════════════════
    # CONVERSATION HISTORY INSPECTION
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_conversation_history(self) -> List[ConversationMessage]:
        """
        Get conversation history
        
        Used by: ζ (Recurrence) operator for encoding
        
        Returns:
            List of ConversationMessage objects
        """
        return self._conversation_history.copy()
    
    def get_conversation_length(self) -> int:
        """Get number of messages in conversation"""
        return len(self._conversation_history)
    
    def get_conversation_tokens(self) -> int:
        """Get total tokens in conversation"""
        return sum(msg.tokens for msg in self._conversation_history)
    
    def add_message(self, role: str, content: str, tokens: int = 0):
        """Add a message to conversation history"""
        self._conversation_history.append(ConversationMessage(
            role=role,
            content=content,
            timestamp=datetime.now(),
            tokens=tokens
        ))
    
    # ═══════════════════════════════════════════════════════════════════════
    # PENDING OPERATIONS INSPECTION
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_pending_operations(self) -> List[OperationInfo]:
        """
        Get pending operations
        
        Used by: Ρ (Perceive) operator
        
        Returns:
            List of OperationInfo objects
        """
        return self._pending_operations.copy()
    
    def get_pending_count(self) -> int:
        """Get number of pending operations"""
        return len(self._pending_operations)
    
    def add_operation(self, op_id: str, op_type: str):
        """Add a pending operation"""
        self._pending_operations.append(OperationInfo(
            id=op_id,
            type=op_type,
            status='pending',
            started_at=datetime.now(),
            duration=0.0
        ))
    
    def remove_operation(self, op_id: str):
        """Remove a completed operation"""
        self._pending_operations = [
            op for op in self._pending_operations if op.id != op_id
        ]
    
    # ═══════════════════════════════════════════════════════════════════════
    # SYSTEM RESOURCE INSPECTION
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_cpu_usage(self) -> float:
        """
        Get CPU usage percentage
        
        Used by: χ (Measure) operator
        
        Returns:
            CPU usage as 0-100
        """
        return psutil.cpu_percent(interval=0.1)
    
    def get_memory_usage(self) -> Dict[str, float]:
        """
        Get memory usage
        
        Used by: χ (Measure) operator
        
        Returns:
            Dictionary with memory info (GB)
        """
        memory = psutil.virtual_memory()
        return {
            'total': memory.total / 1e9,
            'available': memory.available / 1e9,
            'used': memory.used / 1e9,
            'percent': memory.percent
        }
    
    def get_disk_usage(self, path: str = '/') -> Dict[str, float]:
        """
        Get disk usage
        
        Used by: χ (Measure) operator
        
        Returns:
            Dictionary with disk info (GB)
        """
        disk = psutil.disk_usage(path)
        return {
            'total': disk.total / 1e9,
            'used': disk.used / 1e9,
            'free': disk.free / 1e9,
            'percent': disk.percent
        }
    
    # ═══════════════════════════════════════════════════════════════════════
    # COMPREHENSIVE STATE SNAPSHOT
    # ═══════════════════════════════════════════════════════════════════════
    
    def get_full_state_snapshot(self) -> Dict[str, Any]:
        """
        Get comprehensive state snapshot
        
        Used by: Ρ (Perceive) operator for full observation
        
        Returns:
            Dictionary with all state information
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'threads': {
                'count': self.get_thread_count(),
                'active': [
                    {'id': t.id, 'name': t.name, 'alive': t.is_alive}
                    for t in self.get_active_threads()
                ]
            },
            'files': {
                'count': self.get_file_count(),
                'open': [
                    {'path': f.path, 'mode': f.mode}
                    for f in self.get_open_files()
                ]
            },
            'gpu': self._gpu_to_dict(self.get_gpu_memory_usage()),
            'model': self.get_model_state(),
            'conversation': {
                'messages': self.get_conversation_length(),
                'tokens': self.get_conversation_tokens()
            },
            'operations': {
                'pending': self.get_pending_count()
            },
            'resources': {
                'cpu': self.get_cpu_usage(),
                'memory': self.get_memory_usage(),
                'disk': self.get_disk_usage()
            }
        }
    
    def _gpu_to_dict(self, gpu_info: Optional[GPUMemoryInfo]) -> Dict:
        """Convert GPUMemoryInfo to dict"""
        if gpu_info is None:
            return {'available': False}
        return {
            'available': True,
            'allocated_gb': gpu_info.allocated,
            'reserved_gb': gpu_info.reserved,
            'free_gb': gpu_info.free,
            'total_gb': gpu_info.total,
            'utilization': gpu_info.utilization
        }
    
    # ═══════════════════════════════════════════════════════════════════════
    # SERIALIZATION
    # ═══════════════════════════════════════════════════════════════════════
    
    def to_json(self) -> str:
        """Serialize state to JSON"""
        return json.dumps(self.get_full_state_snapshot(), indent=2)
    
    def save_to_file(self, path: str):
        """Save state snapshot to file"""
        with open(path, 'w') as f:
            f.write(self.to_json())


# ═══════════════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # Create state inspector
    state = AISystemState()
    
    # Inspect threads
    print("Active Threads:")
    for thread in state.get_active_threads():
        print(f"  - {thread.name} (ID: {thread.id})")
    
    # Inspect GPU
    gpu = state.get_gpu_memory_usage()
    if gpu:
        print(f"\nGPU Memory:")
        print(f"  Allocated: {gpu.allocated:.2f} GB")
        print(f"  Free: {gpu.free:.2f} GB")
        print(f"  Utilization: {gpu.utilization*100:.1f}%")
    
    # Inspect resources
    print(f"\nCPU Usage: {state.get_cpu_usage():.1f}%")
    memory = state.get_memory_usage()
    print(f"Memory: {memory['used']:.2f} / {memory['total']:.2f} GB ({memory['percent']:.1f}%)")
    
    # Full snapshot
    print("\nFull State Snapshot:")
    print(state.to_json())
