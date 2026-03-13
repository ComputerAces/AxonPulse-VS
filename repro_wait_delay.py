import time
import os
import sys
from unittest.mock import MagicMock

# Add project root to path
sys.path.append(os.getcwd())

from axonpulse.core.bridge import AxonPulseBridge
from axonpulse.core.engine.execution_engine import ExecutionEngine
from axonpulse.nodes.lib.wait_node import WaitNode

def test_wait_delay():
    print("--- Testing Wait Node Delay ---")
    import multiprocessing
    manager = multiprocessing.Manager()
    bridge = AxonPulseBridge(manager)
    
    # Mock node object for properties
    mock_node = MagicMock()
    mock_node.properties = {'Milliseconds': 2000}
    mock_node.name = "Wait Test"
    
    # Simulate execution of WaitNode
    # Case 1: Using property
    result = WaitNode(_bridge=bridge, _node=mock_node, _node_id="wait1")
    print(f"WaitNode result (property): {result}")
    
    # Case 2: Using kwargs (wire input)
    result_kwargs = WaitNode(Milliseconds=3000, _bridge=bridge, _node=mock_node, _node_id="wait2")
    print(f"WaitNode result (kwargs): {result_kwargs}")

    # Now verify Engine logic
    engine = ExecutionEngine(bridge)
    
    # Simplified _execute_step logic check
    def get_delay(res):
        if isinstance(res, tuple) and len(res) >= 2 and res[0] == "_YSWAIT":
            return res[1]
        return 0

    delay1 = get_delay(result)
    delay2 = get_delay(result_kwargs)
    
    print(f"Extracted Delay 1: {delay1}ms")
    print(f"Extracted Delay 2: {delay2}ms")

    if delay1 != 2000:
        print(f"FAILURE: Delay 1 should be 2000, got {delay1}")
    if delay2 != 3000:
        print(f"FAILURE: Delay 2 should be 3000, got {delay2}")

    # Test FlowController delay
    from axonpulse.core.flow_controller import FlowController
    fc = FlowController("Start")
    
    # Clear initial queue for clean test
    fc.queue = []
    
    start_time = time.time()
    fc.push("NextNode", [], "Flow", delay=1000)
    
    # Immediately check
    if not fc.queue and len(fc.delayed_queue) == 1:
        print("SUCCESS: Pulse correctly placed in delayed queue.")
    else:
        print(f"FAILURE: Queue state - Q: {len(fc.queue)}, DQ: {len(fc.delayed_queue)}")
        return

    # Wait 0.5s
    time.sleep(0.5)
    node, _, _ = fc.pop()
    if node is None:
        print("SUCCESS: pop() returned None after 0.5s (correctly waiting).")
    else:
        print(f"FAILURE: pop() returned {node} too early!")
        return

    # Wait another 0.6s
    time.sleep(0.6)
    node, _, _ = fc.pop()
    if node == "NextNode":
        print("SUCCESS: pop() returned NextNode after 1.1s total.")
    else:
        print(f"FAILURE: pop() still returned None or wrong node: {node}")
        return

if __name__ == "__main__":
    test_wait_delay()
