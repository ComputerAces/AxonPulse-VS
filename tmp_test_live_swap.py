import time
import threading
import logging
import multiprocessing
from axonpulse.core.bridge import AxonPulseBridge
from axonpulse.core.engine.execution_engine import ExecutionEngine
from axonpulse.nodes.registry import NodeRegistry
import axonpulse.nodes.lib # Trigger registration

# Configure logging to see LiveSwap messages
logging.basicConfig(level=logging.INFO)

def test_live_swap_nested():
    print(f"Registered Labels: {NodeRegistry.get_all_labels()}")
    print("\n--- Testing Nested Live Swap (Propagation) ---")
    manager = multiprocessing.Manager()
    bridge = AxonPulseBridge(manager)
    engine = ExecutionEngine(bridge, headless=True)
    
    # Inner Graph (The one inside the SubGraph)
    inner_v1 = {
        "nodes": [
            {"id": "inner_start", "type": "Start Node", "name": "InnerStart"},
            {"id": "inner_log", "type": "Print", "name": "InnerLog", "properties": {"Message": "NESTED V1"}},
            {"id": "inner_wait", "type": "Wait", "name": "InnerWait", "properties": {"Milliseconds": 1000}}
        ],
        "wires": [
            {"from_node": "inner_start", "from_port": "Flow", "to_node": "inner_log", "to_port": "Flow"},
            {"from_node": "inner_log", "from_port": "Flow", "to_node": "inner_wait", "to_port": "Flow"},
            {"from_node": "inner_wait", "from_port": "Flow", "to_node": "inner_log", "to_port": "Flow"}
        ]
    }

    inner_v2 = {
        "nodes": [
            {"id": "inner_start", "type": "Start Node", "name": "InnerStart"},
            {"id": "inner_log", "type": "Print", "name": "InnerLog", "properties": {"Message": "NESTED V2 SWAPPED!"}},
            {"id": "inner_wait", "type": "Wait", "name": "InnerWait", "properties": {"Milliseconds": 1000}}
        ],
        "wires": [
            {"from_node": "inner_start", "from_port": "Flow", "to_node": "inner_log", "to_port": "Flow"},
            {"from_node": "inner_log", "from_port": "Flow", "to_node": "inner_wait", "to_port": "Flow"},
            {"from_node": "inner_wait", "from_port": "Flow", "to_node": "inner_log", "to_port": "Flow"}
        ]
    }
    
    # Outer Graph
    outer_v1 = {
        "nodes": [
            {"id": "start", "type": "Start Node", "name": "Start"},
            {"id": "subgraph", "type": "SubGraph Node", "name": "Sub", "properties": {"Embedded Data": inner_v1}}
        ],
        "wires": [
            {"from_node": "start", "from_port": "Flow", "to_node": "subgraph", "to_port": "Flow"}
        ]
    }

    outer_v2 = {
        "nodes": [
            {"id": "start", "type": "Start Node", "name": "Start"},
            {"id": "subgraph", "type": "SubGraph Node", "name": "Sub", "properties": {"Embedded Data": inner_v2}}
        ],
        "wires": [
            {"from_node": "start", "from_port": "Flow", "to_node": "subgraph", "to_port": "Flow"}
        ]
    }

    from axonpulse.core.loader import load_graph_data
    load_graph_data(outer_v1, bridge, engine)
    
    def run_engine():
        try:
            engine.run("start")
        except Exception as e:
            print(f"Engine Error: {e}")

    t = threading.Thread(target=run_engine, daemon=True)
    t.start()
    
    print("Engine started with Nested V1. Waiting 3 seconds...")
    time.sleep(3.0)
    
    print("Triggering Live Swap on Parent (which should propagate to Child)...")
    bridge.set("_SYSTEM_LIVE_SWAP_DATA", outer_v2)
    
    time.sleep(4.0)
    
    print("Stopping engine...")
    bridge.set("_SYSTEM_STOP", True)
    t.join(timeout=2.0)
    print("Test Complete. Check logs for 'NESTED V2 SWAPPED!'")

if __name__ == "__main__":
    test_live_swap_nested()
