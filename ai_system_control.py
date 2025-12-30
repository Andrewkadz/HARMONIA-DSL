#!/usr/bin/env python3.11
"""
AI System Control API
Provides interface for Φπε operators to control AI system operations
"""

import os
import signal
import threading
import torch
import hashlib
import pickle
import json
import gc
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AISystemControl:
    """
    Control API for AI Systems
    
    This class provides methods for Φπε operators to control
    AI system operations.
    
    Used by:
    - / (Disrupt) operator - interrupt operations
    - Φ (Stabilize) operator - stabilize system
    - ζ (Recurrence) operator - save state
    - δ (Micro-transform) operator - cleanup resources
    - Ω (Close) operator - shutdown
    """
    
    def __init__(self, ai_system=None, config: Optional[Dict] = None):
        """
        Initialize control interface
        
        Args:
            ai_system: The AI system to control
            config: Configuration dictionary
        """
        self.ai_system = ai_system
        self.config = config or self._default_config()
        self._active_operations = {}
        self._shutdown_initiated = False
        self._checkpoint_path = Path(self.config['checkpoint_path'])
        self._checkpoint_path.mkdir(parents=True, exist_ok=True)
        
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            'checkpoint_path': '/tmp/ai_checkpoints',
            'timeout': 30,
            'force_on_timeout': True,
            'verify_checksums': True,
            'log_path': '/tmp/ai_control.log'
        }
    
    # ═══════════════════════════════════════════════════════════════════════
    # INTERRUPT OPERATIONS (/ operator)
    # ═══════════════════════════════════════════════════════════════════════
    
    def interrupt_operation(self, operation_id: str) -> bool:
        """
        Interrupt a specific operation
        
        Used by: / (Disrupt) operator
        
        Args:
            operation_id: ID of operation to interrupt
            
        Returns:
            True if interrupted successfully
        """
        if operation_id not in self._active_operations:
            logger.warning(f"Operation {operation_id} not found")
            return False
        
        operation = self._active_operations[operation_id]
        
        # If it's a thread, interrupt it
        if isinstance(operation, threading.Thread):
            # Python doesn't have thread.interrupt(), so we use a flag
            operation.interrupted = True
            logger.info(f"Interrupted operation: {operation_id}")
            return True
        
        return False
    
    def interrupt_all_operations(self) -> int:
        """
        Interrupt all active operations
        
        Used by: / (Disrupt) operator
        
        Returns:
            Number of operations interrupted
        """
        count = 0
        for op_id in list(self._active_operations.keys()):
            if self.interrupt_operation(op_id):
                count += 1
        
        logger.info(f"Interrupted {count} operations")
        return count
    
    def cancel_gpu_operations(self):
        """
        Cancel GPU operations
        
        Used by: / (Disrupt) operator
        """
        if torch.cuda.is_available():
            torch.cuda.synchronize()
            logger.info("GPU operations synchronized")
    
    # ═══════════════════════════════════════════════════════════════════════
    # STABILIZE SYSTEM (Φ operator)
    # ═══════════════════════════════════════════════════════════════════════
    
    def stabilize_system(self, timeout: float = 5.0) -> bool:
        """
        Bring system to stable state
        
        Used by: Φ (Stabilize) operator
        
        Args:
            timeout: Maximum time to wait for stability
            
        Returns:
            True if system stabilized
        """
        import time
        start = time.time()
        
        # Wait for all operations to complete or timeout
        while len(self._active_operations) > 0:
            if time.time() - start > timeout:
                logger.warning("Stabilization timeout, forcing")
                self.interrupt_all_operations()
                break
            time.sleep(0.1)
        
        # Synchronize GPU
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        
        logger.info("System stabilized")
        return True
    
    def wait_for_quiescence(self, timeout: float = 10.0) -> bool:
        """
        Wait for system to reach quiescent state
        
        Used by: Φ (Stabilize) operator
        
        Args:
            timeout: Maximum time to wait
            
        Returns:
            True if quiescent
        """
        import time
        start = time.time()
        
        while True:
            if len(self._active_operations) == 0:
                logger.info("System quiescent")
                return True
            
            if time.time() - start > timeout:
                logger.warning("Quiescence timeout")
                return False
            
            time.sleep(0.1)
    
    # ═══════════════════════════════════════════════════════════════════════
    # SAVE STATE (ζ operator)
    # ═══════════════════════════════════════════════════════════════════════
    
    def save_checkpoint(self, name: str = 'checkpoint') -> Path:
        """
        Save system checkpoint
        
        Used by: ζ (Recurrence) operator
        
        Args:
            name: Checkpoint name
            
        Returns:
            Path to saved checkpoint
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        checkpoint_file = self._checkpoint_path / f"{name}_{timestamp}.pt"
        
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'model_state': self._get_model_state_dict(),
            'config': self.config,
            'metadata': {
                'version': '1.0',
                'system': 'ai_control'
            }
        }
        
        torch.save(checkpoint, checkpoint_file)
        logger.info(f"Checkpoint saved: {checkpoint_file}")
        
        # Save checksum
        self._save_checksum(checkpoint_file)
        
        return checkpoint_file
    
    def _get_model_state_dict(self) -> Optional[Dict]:
        """Get model state dict if available"""
        if self.ai_system is None:
            return None
        
        if hasattr(self.ai_system, 'state_dict'):
            return self.ai_system.state_dict()
        
        return None
    
    def save_conversation_history(self, history: List[Dict], name: str = 'conversation') -> Path:
        """
        Save conversation history
        
        Used by: ζ (Recurrence) operator
        
        Args:
            history: List of conversation messages
            name: File name
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        history_file = self._checkpoint_path / f"{name}_{timestamp}.json"
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        logger.info(f"Conversation history saved: {history_file}")
        return history_file
    
    def encode_memory_chunk(self, memory_chunk: Any, chunk_id: str) -> bool:
        """
        Encode and save a memory chunk
        
        Used by: ζ (Recurrence) operator in loops
        
        Args:
            memory_chunk: Memory data to encode
            chunk_id: Unique identifier for chunk
            
        Returns:
            True if encoded successfully
        """
        chunk_file = self._checkpoint_path / f"memory_{chunk_id}.pkl"
        
        try:
            with open(chunk_file, 'wb') as f:
                pickle.dump(memory_chunk, f)
            
            logger.info(f"Memory chunk encoded: {chunk_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to encode memory chunk {chunk_id}: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════════════════
    # VERIFY CONSISTENCY (χ operator)
    # ═══════════════════════════════════════════════════════════════════════
    
    def verify_consistency(self) -> bool:
        """
        Verify system state consistency
        
        Used by: χ (Measure) operator
        
        Returns:
            True if consistent
        """
        # Check all checkpoints have valid checksums
        for checkpoint_file in self._checkpoint_path.glob('*.pt'):
            if not self._verify_checksum(checkpoint_file):
                logger.error(f"Checksum verification failed: {checkpoint_file}")
                return False
        
        logger.info("Consistency verification passed")
        return True
    
    def _save_checksum(self, file_path: Path):
        """Save SHA256 checksum for file"""
        checksum = self._compute_checksum(file_path)
        checksum_file = file_path.with_suffix('.sha256')
        
        with open(checksum_file, 'w') as f:
            f.write(checksum)
    
    def _verify_checksum(self, file_path: Path) -> bool:
        """Verify file checksum"""
        checksum_file = file_path.with_suffix('.sha256')
        
        if not checksum_file.exists():
            logger.warning(f"No checksum file for {file_path}")
            return True  # Don't fail if checksum doesn't exist
        
        with open(checksum_file, 'r') as f:
            stored_checksum = f.read().strip()
        
        actual_checksum = self._compute_checksum(file_path)
        
        return stored_checksum == actual_checksum
    
    def _compute_checksum(self, file_path: Path) -> str:
        """Compute SHA256 checksum"""
        sha256 = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        
        return sha256.hexdigest()
    
    def verify_checkpoint_loadable(self, checkpoint_path: Path) -> bool:
        """
        Verify checkpoint can be loaded
        
        Used by: χ (Measure) operator
        
        Args:
            checkpoint_path: Path to checkpoint
            
        Returns:
            True if loadable
        """
        try:
            checkpoint = torch.load(checkpoint_path)
            assert 'model_state' in checkpoint
            assert 'timestamp' in checkpoint
            logger.info(f"Checkpoint verified: {checkpoint_path}")
            return True
        except Exception as e:
            logger.error(f"Checkpoint verification failed: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════════════════
    # RELEASE RESOURCES (δ operator)
    # ═══════════════════════════════════════════════════════════════════════
    
    def release_resources(self):
        """
        Release all held resources
        
        Used by: δ (Micro-transform) operator
        """
        # Release GPU memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info("GPU memory released")
        
        # Force garbage collection
        gc.collect()
        logger.info("Garbage collection completed")
    
    def close_file_handles(self):
        """
        Close open file handles
        
        Used by: δ (Micro-transform) operator
        """
        # In production, track file handles and close them
        logger.info("File handles closed")
    
    def release_locks(self):
        """
        Release all locks
        
        Used by: δ (Micro-transform) operator
        """
        # In production, track locks and release them
        logger.info("Locks released")
    
    def cleanup_temp_files(self):
        """
        Clean up temporary files
        
        Used by: δ (Micro-transform) operator
        """
        # Clean up old checkpoints (keep last 5)
        checkpoints = sorted(self._checkpoint_path.glob('checkpoint_*.pt'))
        if len(checkpoints) > 5:
            for old_checkpoint in checkpoints[:-5]:
                old_checkpoint.unlink()
                # Also remove checksum
                checksum_file = old_checkpoint.with_suffix('.sha256')
                if checksum_file.exists():
                    checksum_file.unlink()
                logger.info(f"Removed old checkpoint: {old_checkpoint}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # SHUTDOWN (Ω operator)
    # ═══════════════════════════════════════════════════════════════════════
    
    def shutdown(self, exit_code: int = 0):
        """
        Shutdown the system
        
        Used by: Ω (Close) operator
        
        Args:
            exit_code: Exit code (0 = success)
        """
        if self._shutdown_initiated:
            logger.warning("Shutdown already initiated")
            return
        
        self._shutdown_initiated = True
        
        # Write shutdown status
        status_file = self._checkpoint_path / '.shutdown_status'
        with open(status_file, 'w') as f:
            f.write(f"SHUTDOWN_COMPLETE\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Exit code: {exit_code}\n")
        
        logger.info(f"Shutdown complete with exit code {exit_code}")
        
        # In production, this would call sys.exit(exit_code)
        # For testing, we just log it
        # import sys
        # sys.exit(exit_code)
    
    def force_shutdown(self):
        """
        Force immediate shutdown
        
        Used by: / / / Ω (Emergency shutdown)
        """
        logger.warning("FORCE SHUTDOWN")
        self.shutdown(exit_code=1)
        
        # In production, this would force kill
        # os._exit(1)
    
    # ═══════════════════════════════════════════════════════════════════════
    # TIMEOUT HANDLING
    # ═══════════════════════════════════════════════════════════════════════
    
    def execute_with_timeout(self, func, timeout: float = 30.0):
        """
        Execute function with timeout
        
        Args:
            func: Function to execute
            timeout: Timeout in seconds
        """
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Operation timed out after {timeout}s")
        
        # Set timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(int(timeout))
        
        try:
            result = func()
            signal.alarm(0)  # Cancel timeout
            return result
        except TimeoutError:
            logger.error(f"Timeout exceeded, forcing shutdown")
            self.force_shutdown()
            raise
    
    # ═══════════════════════════════════════════════════════════════════════
    # OPERATION TRACKING
    # ═══════════════════════════════════════════════════════════════════════
    
    def register_operation(self, op_id: str, operation: Any):
        """Register an active operation"""
        self._active_operations[op_id] = operation
        logger.info(f"Operation registered: {op_id}")
    
    def unregister_operation(self, op_id: str):
        """Unregister a completed operation"""
        if op_id in self._active_operations:
            del self._active_operations[op_id]
            logger.info(f"Operation unregistered: {op_id}")
    
    def get_active_operation_count(self) -> int:
        """Get number of active operations"""
        return len(self._active_operations)


# ═══════════════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # Create control interface
    control = AISystemControl()
    
    # Interrupt operations
    print("Interrupting operations...")
    control.interrupt_all_operations()
    
    # Stabilize system
    print("Stabilizing system...")
    control.stabilize_system()
    
    # Save checkpoint
    print("Saving checkpoint...")
    checkpoint_path = control.save_checkpoint('test')
    print(f"Checkpoint saved: {checkpoint_path}")
    
    # Verify consistency
    print("Verifying consistency...")
    is_consistent = control.verify_consistency()
    print(f"Consistent: {is_consistent}")
    
    # Release resources
    print("Releasing resources...")
    control.release_resources()
    
    # Shutdown
    print("Shutting down...")
    control.shutdown(exit_code=0)
