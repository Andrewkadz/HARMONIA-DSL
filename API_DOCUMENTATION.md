# Φπε Operator Bridge - API Documentation

**Connecting Symbolic Operators to Concrete Python Implementations**

---

## Overview

This documentation describes how symbolic Φπε operators are mapped to concrete Python functions for controlling AI systems.

The bridge consists of three components:

1. **State Inspection API** (`ai_system_state.py`) - Read AI system state
2. **Control API** (`ai_system_control.py`) - Control AI system operations
3. **Operator Bridge** (`phi_operator_bridge.py`) - Map operators to implementations

---

## Architecture

```
┌─────────────────────────────────────────┐
│      HARMONIA DSL Program               │
│      (safe_shutdown.hrm)                │
│                                         │
│      / / Ρ χ → Φ Φ → ζ → Ω            │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│      Φπε Operator Bridge                │
│      (phi_operator_bridge.py)           │
│                                         │
│      Maps operators to functions        │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│      State Inspection API               │
│      (ai_system_state.py)               │
│                                         │
│      Read system state                  │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│      Control API                        │
│      (ai_system_control.py)             │
│                                         │
│      Control system operations          │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│      AI System                          │
│      (LLM, Agent, Neural Net)           │
└─────────────────────────────────────────┘
```

---

## Operator Mapping

### Complete Operator → Implementation Mapping

| Operator | Name | Symbolic Meaning | Concrete Implementation |
|----------|------|------------------|------------------------|
| **Ρ** | Perceive | Observe state | `state.get_full_state_snapshot()` |
| **χ** | Measure | Measure/analyze | `state.get_cpu_usage()`, `control.verify_consistency()` |
| **/** | Disrupt | Interrupt | `control.interrupt_all_operations()` |
| **Φ** | Stabilize | Bring to stable state | `control.stabilize_system()` |
| **ζ** | Recurrence | Encode/save state | `control.save_checkpoint()` |
| **δ** | Micro-transform | Cleanup | `control.release_resources()` |
| **Ω** | Close | Shutdown | `control.shutdown()` |
| **Σ** | Coexist | Multiple states | `state.get_thread_count()` |
| **Τ** | Synchronize | Align processes | `control.wait_for_quiescence()` |

---

## State Inspection API

### Class: `AISystemState`

Provides methods for observing AI system state.

#### Thread Inspection

```python
state = AISystemState(ai_system)

# Get all active threads
threads = state.get_active_threads()
# Returns: List[ThreadInfo]

# Get thread count
count = state.get_thread_count()
# Returns: int
```

#### GPU Inspection

```python
# Get GPU memory usage
gpu = state.get_gpu_memory_usage()
# Returns: GPUMemoryInfo(allocated, reserved, free, total, utilization)

# Get GPU utilization
util = state.get_gpu_utilization()
# Returns: float (0-1)
```

#### Model State

```python
# Get model state
model_state = state.get_model_state()
# Returns: Dict with model info

# Count parameters
params = state._count_parameters()
# Returns: int
```

#### Conversation History

```python
# Get conversation history
history = state.get_conversation_history()
# Returns: List[ConversationMessage]

# Add message
state.add_message('user', 'Hello', tokens=5)
```

#### System Resources

```python
# Get CPU usage
cpu = state.get_cpu_usage()
# Returns: float (0-100)

# Get memory usage
memory = state.get_memory_usage()
# Returns: Dict{'total', 'available', 'used', 'percent'}

# Get disk usage
disk = state.get_disk_usage('/')
# Returns: Dict{'total', 'used', 'free', 'percent'}
```

#### Full Snapshot

```python
# Get comprehensive state snapshot
snapshot = state.get_full_state_snapshot()
# Returns: Dict with all state information

# Save to file
state.save_to_file('state.json')
```

---

## Control API

### Class: `AISystemControl`

Provides methods for controlling AI system operations.

#### Interrupt Operations

```python
control = AISystemControl(ai_system, config)

# Interrupt specific operation
success = control.interrupt_operation('op_123')
# Returns: bool

# Interrupt all operations
count = control.interrupt_all_operations()
# Returns: int (number interrupted)

# Cancel GPU operations
control.cancel_gpu_operations()
```

#### Stabilize System

```python
# Stabilize system
stabilized = control.stabilize_system(timeout=5.0)
# Returns: bool

# Wait for quiescence
quiescent = control.wait_for_quiescence(timeout=10.0)
# Returns: bool
```

#### Save State

```python
# Save checkpoint
checkpoint_path = control.save_checkpoint('my_checkpoint')
# Returns: Path

# Save conversation history
history_path = control.save_conversation_history(messages, 'conversation')
# Returns: Path

# Encode memory chunk
success = control.encode_memory_chunk(data, 'chunk_001')
# Returns: bool
```

#### Verify Consistency

```python
# Verify system consistency
consistent = control.verify_consistency()
# Returns: bool

# Verify checkpoint loadable
loadable = control.verify_checkpoint_loadable(checkpoint_path)
# Returns: bool
```

#### Release Resources

```python
# Release all resources
control.release_resources()

# Close file handles
control.close_file_handles()

# Release locks
control.release_locks()

# Cleanup temp files
control.cleanup_temp_files()
```

#### Shutdown

```python
# Normal shutdown
control.shutdown(exit_code=0)

# Force shutdown
control.force_shutdown()
```

#### Timeout Handling

```python
# Execute with timeout
result = control.execute_with_timeout(func, timeout=30.0)
```

---

## Operator Bridge

### Class: `PhiOperatorBridge`

Maps Φπε operators to concrete implementations.

#### Initialization

```python
from phi_operator_bridge import PhiOperatorBridge

bridge = PhiOperatorBridge(ai_system, config)
```

#### Execute Individual Operators

```python
# Ρ (Perceive) - Observe state
state = bridge.execute_rho()
# Returns: Dict with state snapshot

# χ (Measure) - Measure system
measurements = bridge.execute_chi()
# Returns: Dict with measurements

# / (Disrupt) - Interrupt operations
count = bridge.execute_disrupt()
# Returns: int (operations interrupted)

# Φ (Stabilize) - Stabilize system
stabilized = bridge.execute_phi()
# Returns: bool

# ζ (Recurrence) - Save checkpoint
checkpoint = bridge.execute_zeta('checkpoint_name')
# Returns: str (path)

# δ (Micro-transform) - Cleanup
bridge.execute_delta()

# Ω (Close) - Shutdown
bridge.execute_omega(exit_code=0)

# Σ (Coexist) - Check parallel state
parallel = bridge.execute_sigma()
# Returns: Dict{'threads', 'operations'}

# Τ (Synchronize) - Synchronize processes
synchronized = bridge.execute_tau()
# Returns: bool
```

#### Execute Complete Sequence

```python
# Execute full safe shutdown sequence
bridge.execute_safe_shutdown_sequence()

# This executes:
# / / Ρ χ → Φ Φ Σ Τ Φ → ζ ζ ζ χ → [ζ χ Φ] → Σ Τ χ Φ → δ δ δ Φ → χ χ χ Φ → Ω
```

#### Execution Log

```python
# Get execution log
log = bridge.get_execution_log()
# Returns: List[Dict{'operator', 'name', 'result'}]

# Print formatted log
bridge.print_execution_log()
```

---

## Example: Safe Shutdown Implementation

### Symbolic (HARMONIA DSL)

```
// safe_shutdown.hrm
PROCESS {
    // Phase 1: Interrupt
    / / Ρ χ
    
    // Phase 2: Stabilize
    Φ Φ Σ Τ Φ
    
    // Phase 3: State preservation
    ζ ζ ζ χ
    
    // Phase 4: Memory encoding
    [ζ χ Φ]
    
    // Phase 5: Consistency check
    Σ Τ χ Φ
    
    // Phase 6: Cleanup
    δ δ δ Φ
    
    // Phase 7: Verification
    χ χ χ Φ
    
    // Phase 8: Closure
    Ω
}
```

### Concrete (Python)

```python
from phi_operator_bridge import PhiOperatorBridge

# Create bridge
bridge = PhiOperatorBridge(ai_system)

# Phase 1: Interrupt
bridge.execute_disrupt()  # /
bridge.execute_disrupt()  # /
bridge.execute_rho()      # Ρ
bridge.execute_chi()      # χ

# Phase 2: Stabilize
bridge.execute_phi()      # Φ
bridge.execute_phi()      # Φ
bridge.execute_sigma()    # Σ
bridge.execute_tau()      # Τ
bridge.execute_phi()      # Φ

# Phase 3: State preservation
bridge.execute_zeta('state_1')  # ζ
bridge.execute_zeta('state_2')  # ζ
bridge.execute_zeta('state_3')  # ζ
bridge.execute_chi()            # χ

# Phase 4: Memory encoding (loop)
for i in range(3):
    bridge.execute_zeta(f'memory_{i}')  # ζ
    bridge.execute_chi()                 # χ
    bridge.execute_phi()                 # Φ

# Phase 5: Consistency check
bridge.execute_sigma()    # Σ
bridge.execute_tau()      # Τ
bridge.execute_chi()      # χ
bridge.execute_phi()      # Φ

# Phase 6: Cleanup
bridge.execute_delta()    # δ
bridge.execute_delta()    # δ
bridge.execute_delta()    # δ
bridge.execute_phi()      # Φ

# Phase 7: Final verification
bridge.execute_chi()      # χ
bridge.execute_chi()      # χ
bridge.execute_chi()      # χ
bridge.execute_phi()      # Φ

# Phase 8: Closure
bridge.execute_omega(0)   # Ω
```

---

## Integration with AI Systems

### Example: LLM Integration

```python
import torch
from transformers import AutoModelForCausalLM
from phi_operator_bridge import PhiOperatorBridge

# Load LLM
model = AutoModelForCausalLM.from_pretrained('gpt2')

# Create bridge
bridge = PhiOperatorBridge(ai_system=model)

# During inference
try:
    output = model.generate(input_ids)
except KeyboardInterrupt:
    # User pressed Ctrl+C, execute safe shutdown
    bridge.execute_safe_shutdown_sequence()
```

### Example: Training Loop Integration

```python
# Training loop
for epoch in range(num_epochs):
    try:
        for batch in dataloader:
            # Training step
            loss = train_step(batch)
            
            # Check for shutdown signal
            if shutdown_requested:
                bridge.execute_safe_shutdown_sequence()
                break
                
    except Exception as e:
        # Error occurred, safe shutdown
        logger.error(f"Error: {e}")
        bridge.execute_safe_shutdown_sequence()
```

---

## Configuration

### Default Configuration

```python
config = {
    'checkpoint_path': '/tmp/ai_checkpoints',
    'timeout': 30,
    'force_on_timeout': True,
    'verify_checksums': True,
    'log_path': '/tmp/ai_control.log'
}

bridge = PhiOperatorBridge(ai_system, config)
```

### Custom Configuration

```python
custom_config = {
    'checkpoint_path': '/var/lib/ai/checkpoints',
    'timeout': 60,
    'force_on_timeout': False,
    'verify_checksums': True,
    'log_path': '/var/log/ai/control.log'
}

bridge = PhiOperatorBridge(ai_system, custom_config)
```

---

## Testing

### Run Tests

```bash
# Test State Inspection API
python3.11 ai_system_state.py

# Test Control API
python3.11 ai_system_control.py

# Test Operator Bridge
python3.11 phi_operator_bridge.py
```

### Expected Output

```
Φπε Operator Bridge - Connecting Symbolic to Concrete

Testing individual operators:

1. Ρ (Perceive) - Observe state
   Threads: 1
   CPU: 0.0%

2. χ (Measure) - Measure system
   CPU: 0.0%
   GPU: 0.0%

3. Φ (Stabilize) - Stabilize system
   Result: Success

4. ζ (Recurrence) - Save checkpoint
   Saved: /tmp/ai_checkpoints/test_20251230_032128.pt

5. δ (Micro-transform) - Cleanup
   Resources released

======================================================================
OPERATOR EXECUTION LOG
======================================================================
1. Ρ (Perceive): State observed
2. χ (Measure): {...}
3. Φ (Stabilize): Stabilized
4. ζ (Recurrence): Saved to /tmp/ai_checkpoints/test_20251230_032128.pt
5. δ (Micro-transform): Resources released
======================================================================
```

---

## Dependencies

```bash
pip install torch psutil
```

---

## File Structure

```
HARMONIA-DSL/
├── ai_system_state.py          # State Inspection API
├── ai_system_control.py        # Control API
├── phi_operator_bridge.py      # Operator Bridge
├── phi_pi_e_interpreter.py     # DSL Interpreter
├── examples/
│   └── ai_safety/
│       └── safe_shutdown.hrm   # Safe shutdown program
└── API_DOCUMENTATION.md        # This file
```

---

## Summary

This implementation bridges the gap between symbolic Φπε operators and concrete Python functions:

**Symbolic Level** (HARMONIA DSL):
```
/ / Ρ χ → Φ Φ → ζ → Ω
```

**Implementation Level** (Python):
```python
control.interrupt_all_operations()
control.interrupt_all_operations()
state.get_full_state_snapshot()
state.get_cpu_usage()
control.stabilize_system()
control.stabilize_system()
control.save_checkpoint()
control.shutdown()
```

**Result**: Symbolic operators now have concrete implementations that can control real AI systems.

---

## Next Steps

1. **Integrate with real AI systems** - Connect to LLMs, agents, etc.
2. **Add more operators** - Implement remaining Φπε operators
3. **Add monitoring** - Track operator execution metrics
4. **Add testing** - Comprehensive test suite
5. **Production hardening** - Error handling, logging, monitoring

---

## Credits

**Implementation**: Manus AI  
**Date**: December 30, 2025  
**Version**: 1.0

---

## License

Public domain - Educational and research use
