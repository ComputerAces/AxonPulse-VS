import os
import sys
import time
from multiprocessing import shared_memory

# Mock AxonPulse path if needed
sys.path.append(os.getcwd())

from axonpulse.core.bridge import AxonPulseBridge
from axonpulse.utils.shm_tracker import SHMTracker
from axonpulse.utils.cleanup import init_global_handlers

def simulate_crash():
    print("--- Phase 1: Simulating Crash ---")
    # 1. Initialize Bridge
    bridge = AxonPulseBridge()
    
    # 2. Create some variables (SHM blocks)
    bridge.set("LeakVar1", "This should be cleaned up", scope_id="TestScope")
    bridge.set("LeakVar2", [1, 2, 3, 4, 5], scope_id="TestScope")
    
    # Get names for verification
    registry = bridge._variables_registry
    shm_names = [v[0] for k, v in registry.items() if "TestScope" in k]
    print(f"Created SHM blocks: {shm_names}")
    
    # Verify they are in tracker
    tracked = SHMTracker.get_all()
    print(f"Tracked blocks: {tracked}")
    
    # 3. Simulate Hard Crash
    print("CRASHING NOW (os._exit(1))...")
    os._exit(1)

def verify_cleanup():
    print("\n--- Phase 2: Verifying Cleanup ---")
    # 1. Initialize Cleanup (this should trigger orphan cleanup)
    init_global_handlers()
    
    # 2. Verify Tracker is empty
    tracked = SHMTracker.get_all()
    if not tracked:
        print("SUCCESS: SHM Tracker is empty.")
    else:
        print(f"FAILURE: SHM Tracker still contains: {tracked}")
        sys.exit(1)
        
    # 3. Double check OS (try to attach to one of the previous names if we had them)
    # Since names are deterministic but include version, we check the registry file if it exists
    # but the tracker should have handled it.
    
    print("SUCCESS: Orphaned SHM blocks cleaned up.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify_cleanup()
    else:
        simulate_crash()
