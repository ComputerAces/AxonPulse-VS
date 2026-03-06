from axonpulse.utils.logger import setup_logger
from axonpulse.core.data import ErrorObject

logger = setup_logger("AxonPulseEngine")

class DebugMixin:
    """
    Handles Debugging, Panics, and Error Routing.
    """
    def _handle_panic(self, error, failing_node, context_stack, start_node_id, inputs=None):
        """
        Routes unhandled exceptions to the Start Node's 'Panic' port if wired.
        Returns True if a Panic handler was found and invoked, False otherwise.
        """
        # Store error details on bridge for LastErrorNode to retrieve
        error_name = type(error).__name__
        error_code = self.context_manager.error_mapping.get(error_name, 999)
        
        # [panic] Create Complex Error Object
        # We try to get project name from bridge or node?
        project_name = self.bridge.get("_META_PROJECT_NAME") or "Unknown Project"
        
        error_obj = ErrorObject(
            project_name=project_name,
            node_name=failing_node.name,
            inputs=inputs,
            error_details=str(error)
        )
        
        self.bridge.bubble_set("_SYSTEM_LAST_ERROR_OBJECT", error_obj, "Engine")
        
        self.bridge.bubble_set("_SYSTEM_LAST_ERROR_CODE", error_code, "Engine")
        self.bridge.bubble_set("_SYSTEM_LAST_ERROR_MESSAGE", str(error), "Engine")
        self.bridge.bubble_set("_SYSTEM_LAST_ERROR_NODE", failing_node.node_id, "Engine")
        self.bridge.bubble_set("_SYSTEM_LAST_ERROR_NODE_NAME", failing_node.name, "Engine")
        
        # [NEW] Visually trace the wire that caused the crash
        # The node was triggered by a specific wire, but ExecutionEngine only passes `inputs` (dict) or nothing.
        # However, we can use the `failing_node.node_id` and the most recently executed nodes if needed.
        # For an exact match, we need to know what triggered it. The UI can trace backwards if needed, 
        # but the easiest way is checking the `context_stack` or finding incoming wires to this node.
        if hasattr(self, 'flow') and hasattr(self.flow, '_last_triggered_wire'):
            last_wire = self.flow._last_triggered_wire
            if last_wire and last_wire.get('to_node') == failing_node.node_id:
                # Format: "{from_node}:{from_port} -> {to_node}:{to_port}"
                wire_str = f"{last_wire['from_node']}:{last_wire['from_port']} -> {last_wire['to_node']}:{last_wire['to_port']}"
                self.bridge.bubble_set("_SYSTEM_LAST_ERROR_WIRE", wire_str, "Engine")
        
        # Explicit Console Error Output
        print("\n" + "="*60)
        print(f" [CRITICAL ERROR] {error_name} in '{failing_node.name}'")
        print(f" MESSAGE: {str(error)}")
        print("="*60 + "\n", flush=True)
        
        # Find wires from Start Node's Error Flow port (Case-Insensitive match)
        panic_wires = [
            w for w in self.wires
            if w["from_node"] == start_node_id and str(w.get("from_port", "")).lower() in ["error flow", "error", "panic"]
        ]
        
        if panic_wires:
            print(f"[DEBUG] [PANIC] Routing to Error Flow handler from Start Node (ID: {start_node_id})...", flush=True)
            self.bridge.set("_PANICKED", True, "Engine") # Signal that we entered panic mode
            for w in panic_wires:
                print(f"[DEBUG] [PANIC] -> {w['to_node']}:{w['to_port']}", flush=True)
                self.flow.push(w["to_node"], [], w["to_port"])
                # Panic pulses run in ROOT scope
                self._increment_scope_count([], 1)
            return True
        else:
            print(f"[DEBUG] [PANIC] No Error Flow wired from Start Node (ID: {start_node_id}). Raising error.", flush=True)
            logger.warning(f"UNHANDLED PANIC in {failing_node.name}: {error}")
            return False
