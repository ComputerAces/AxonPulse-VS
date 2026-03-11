from axonpulse.core.super_node import SuperNode
from axonpulse.nodes.registry import NodeRegistry
from axonpulse.core.types import DataType
import os

@NodeRegistry.register("Breakpoint", "Flow/Debug")
class BreakpointNode(SuperNode):
    """
    Temporarily pauses graph execution at this point, allowing manual inspection of state.
    Execution can be resumed by the user through the UI or by deleting the pause signal file.
    Skipped automatically in Headless mode.
    
    Inputs:
    - Flow: Trigger execution to pause here.
    
    Outputs:
    - Flow: Triggered immediately (Engine handles the pause step contextually).
    """
    version = "2.1.0"

    def __init__(self, node_id, name, bridge):
        super().__init__(node_id, name, bridge)
        self.is_native = True
        self.define_schema()
        self.register_handlers()

    def register_handlers(self):
        self.register_handler("Flow", self.pause)
    
    def define_schema(self):
        self.input_schema = {
            "Flow": DataType.FLOW
        }
        self.output_schema = {
            "Flow": DataType.FLOW
        }

    def pause(self, **kwargs):
        # 1. Check Headless
        headless = self.bridge.get("_SYSTEM_HEADLESS")
        if headless:
            self.logger.info("Breakpoint skipped (Headless Mode).")
            self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
            return True
            
        # 2. Trigger Pause natively via Bridge
        try:
            self.logger.warning(f"Breakpoint hit in {self.name}. Halting Execution Engine.")
            
            # Send Data to UI
            self.bridge.set("_AXON_BREAKPOINT_NODE_NAME", self.name, self.name)
            # Find the most recently triggered wire for diagnostic payloads
            # Engine will capture the active path and set it to "_AXON_BREAKPOINT_DATA" next cycle.
            
            # Activate the Stop
            self.bridge.set("_AXON_BREAKPOINT_ACTIVE", True, self.name)
            
            # We return a Yield signal so the Execution Engine naturally halts and
            # enters its wait-loop on the very next cycle when it checks the bridge.
            self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
            return ("_YSYIELD",)
            
        except Exception as e:
            self.logger.error(f"Failed to trigger Breakpoint: {e}")
            self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
            return True
