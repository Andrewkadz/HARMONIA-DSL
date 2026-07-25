"""
CoherentFlow: ANIMUS-Gated Task Scheduler
=========================================

A real-world application of the ANIMUS Paradigm.
This scheduler manages a pool of workers for heavy tasks, but instead of
using a fixed number of threads, it uses a Harmonic Swarm to measure
system coherence and dynamically gate concurrency.

Key Feature:
- Maximizes throughput when system is stable (High ANIMUS)
- Instantly throttles when system shows stress (Low ANIMUS)
- Prevents system freeze/lag even under 100% load

Usage:
    scheduler = CoherentFlowScheduler(max_workers=16)
    scheduler.submit(my_heavy_task, arg1, arg2)
    scheduler.run()
"""

import time
import psutil
import threading
import queue
import numpy as np
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass
from typing import Callable, List, Any, Dict

# Import the Harmonic Swarm engine
# (Assuming pure_harmonic_swarm.py is in the same directory)
from pure_harmonic_swarm import HarmonicSwarm

@dataclass
class Task:
    id: int
    fn: Callable
    args: tuple
    kwargs: dict
    future: Future = None

class CoherentFlowScheduler:
    def __init__(self, max_workers: int = 8, swarm_size: int = 17):
        self.max_workers = max_workers
        self.task_queue = queue.Queue()
        self.active_tasks: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.is_running = False
        
        # The ANIMUS Engine
        self.swarm = HarmonicSwarm(n_agents=swarm_size)
        self.animus_history: List[float] = []
        self.concurrency_history: List[int] = []
        
        # Executor
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.Lock()
        
        # Metrics
        self.start_time = 0
        self.total_tasks = 0

    def submit(self, fn: Callable, *args, **kwargs):
        """Add a task to the queue."""
        task = Task(id=self.total_tasks, fn=fn, args=args, kwargs=kwargs)
        self.task_queue.put(task)
        self.total_tasks += 1
        return task

    def _measure_system_stress(self) -> float:
        """
        Measure external system stress to perturb the swarm.
        Returns a value 0.0 (calm) to 1.0 (stressed).
        """
        # CPU usage (blocking call, but short)
        cpu = psutil.cpu_percent(interval=None) / 100.0
        
        # Memory pressure
        mem = psutil.virtual_memory().percent / 100.0
        
        # Load average (normalized roughly by CPU count)
        load_avg = psutil.getloadavg()[0] / psutil.cpu_count()
        
        # Composite stress score
        stress = (0.4 * cpu) + (0.4 * load_avg) + (0.2 * mem)
        return min(stress, 1.0)

    def _update_animus(self):
        """
        Update the Harmonic Swarm and compute ANIMUS budget.
        The swarm is perturbed by system stress.
        """
        stress = self._measure_system_stress()
        
        # Perturb swarm based on stress
        # High stress adds "noise" (entropy) to agent phases
        if stress > 0.5:
            perturbation = (stress - 0.5) * 0.5
            for agent in self.swarm.agents:
                agent.psi += np.random.uniform(-perturbation, perturbation)
        
        # Step the swarm
        self.swarm.step(dt=0.05)
        
        # Compute ANIMUS metrics
        stats = self.swarm.get_statistics()
        coherence = stats['coherence']
        
        # ANIMUS Budget = Coherence * (1 - Stress)
        # If system is stressed, budget drops.
        # If swarm is incoherent, budget drops.
        animus = coherence * (1.0 - (stress * 0.5))
        
        return animus, coherence, stress

    def _get_target_concurrency(self, animus: float) -> int:
        """
        Determine how many workers should be active based on ANIMUS.
        """
        if animus >= 0.8:
            # High Coherence: Full Speed
            return self.max_workers
        elif animus >= 0.6:
            # Moderate: 75% Speed
            return max(1, int(self.max_workers * 0.75))
        elif animus >= 0.4:
            # Low: 50% Speed
            return max(1, int(self.max_workers * 0.50))
        elif animus >= 0.2:
            # Critical: 25% Speed
            return max(1, int(self.max_workers * 0.25))
        else:
            # Collapse: Stabilization Mode (1 worker)
            return 1

    def run(self, monitor_interval: float = 0.1):
        """Main scheduler loop."""
        self.is_running = True
        self.start_time = time.time()
        
        print(f"Starting CoherentFlow (Max Workers: {self.max_workers})...")
        
        try:
            while self.is_running:
                # 1. Update ANIMUS
                animus, coherence, stress = self._update_animus()
                self.animus_history.append(animus)
                
                # 2. Determine Policy
                target_concurrency = self._get_target_concurrency(animus)
                self.concurrency_history.append(target_concurrency)
                
                # 3. Manage Workers
                with self.lock:
                    # Clean up finished tasks
                    self.active_tasks = [t for t in self.active_tasks if not t.future.done()]
                    current_count = len(self.active_tasks)
                    
                    # Launch new tasks if budget allows
                    slots_available = target_concurrency - current_count
                    
                    if slots_available > 0 and not self.task_queue.empty():
                        for _ in range(slots_available):
                            if self.task_queue.empty():
                                break
                            task = self.task_queue.get()
                            task.future = self.executor.submit(task.fn, *task.args, **task.kwargs)
                            self.active_tasks.append(task)
                            
                # 4. Monitoring Output
                status = "🟢" if animus > 0.7 else "🟡" if animus > 0.4 else "🔴"
                print(f"\r{status} ANIMUS: {animus:.2f} | Stress: {stress:.2f} | "
                      f"Workers: {current_count}/{target_concurrency} | "
                      f"Queue: {self.task_queue.qsize()} ", end="", flush=True)
                
                # Check if done
                if self.task_queue.empty() and len(self.active_tasks) == 0:
                    print("\nAll tasks completed.")
                    break
                    
                time.sleep(monitor_interval)
                
        except KeyboardInterrupt:
            print("\nStopping scheduler...")
        finally:
            self.executor.shutdown(wait=True)
            self.is_running = False

    def get_report(self):
        """Return execution statistics."""
        duration = time.time() - self.start_time
        avg_animus = np.mean(self.animus_history)
        avg_concurrency = np.mean(self.concurrency_history)
        
        return {
            "duration": duration,
            "tasks_completed": self.total_tasks,
            "throughput": self.total_tasks / duration,
            "avg_animus": avg_animus,
            "avg_concurrency": avg_concurrency
        }

if __name__ == "__main__":
    # Simple self-test
    def dummy_work(duration):
        time.sleep(duration)
        return duration * 2

    scheduler = CoherentFlowScheduler(max_workers=4)
    for i in range(20):
        scheduler.submit(dummy_work, 0.5)
    
    scheduler.run()
    print(scheduler.get_report())
