import os
import sys
from unittest.mock import MagicMock
import multiprocessing

# Add project root to path
sys.path.append(os.getcwd())

from axonpulse.core.bridge import AxonPulseBridge
from axonpulse.nodes.decorators import axon_node, DecoratedNode

def test_decorated_signal_swallowing():
    print("--- Testing DecoratedNode Signal Swallowing ---")
    
    manager = multiprocessing.Manager()
    bridge = AxonPulseBridge(manager)
    
    # Define a test node function
    @axon_node(category="Test", version="1.0.0")
    def SignalNode(Delay: int = 1000):
        return ("_YSWAIT", Delay, True)

    # The decorator registers it, but we can also instantiate a DecoratedNode manually for testing
    def mock_func(Delay=1000):
        return ("_YSWAIT", Delay, True)
    
    node = DecoratedNode("test_id", "SignalNode", bridge, mock_func, "Test", "1.0.0")
    node.define_schema()
    
    # Simulate the call that common/engine would make
    # The handler for 'Flow' is run_decorated_func
    result = node.run_decorated_func(Delay=10000)
    
    print(f"Result from run_decorated_func: {result}")
    
    if result == True:
        print("FAILURE: Signal was swallowed and replaced with True!")
    elif isinstance(result, tuple) and result[0] == "_YSWAIT":
        print("SUCCESS: Signal was passed through correctly.")
    else:
        print(f"UNCERTAIN: Got unexpected result type: {type(result)} -> {result}")

if __name__ == "__main__":
    test_decorated_signal_swallowing()
