from axonpulse.core.super_node import SuperNode
from axonpulse.nodes.registry import NodeRegistry
from axonpulse.core.types import DataType

@NodeRegistry.register("Global Var Set", "Workflow/Variables")
class GlobalVarSetNode(SuperNode):
    """
    Sets a variable at the global (root) level, accessible by any graph or subgraph.
    If the variable doesn't exist, it is created.
    
    ### Inputs:
    - Flow (flow): Trigger the update.
    - Var Name (string): The name of the variable.
    - Value (any): The value to set.
    
    ### Outputs:
    - Flow (flow): Pulse triggered after the variable is set.
    """
    version = "2.1.0"

    def __init__(self, node_id, name, bridge):
        super().__init__(node_id, name, bridge)
        self.is_native = True
        self.properties["Var Name"] = ""
        self.properties["Value"] = None
        self.define_schema()
        self.register_handlers()

    def register_handlers(self):
        self.register_handler("Flow", self.do_work)

    def define_schema(self):
        self.input_schema = {
            "Flow": DataType.FLOW,
            "Var Name": DataType.STRING,
            "Value": DataType.ANY
        }
        self.output_schema = {
            "Flow": DataType.FLOW
        }

    def do_work(self, **kwargs):
        name = kwargs.get("Var Name") or self.properties.get("Var Name")
        val = kwargs.get("Value") or self.properties.get("Value")
        
        if not name:
            self.logger.warning("Global Var Set: No variable name provided.")
            self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
            return True

        # bubble_set ensures it reaches the root registry
        self.bridge.bubble_set(name, val, source_node_id=self.node_id, scope_id="Global")
        self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
        return True

@NodeRegistry.register("Global Var Get", "Workflow/Variables")
class GlobalVarGetNode(SuperNode):
    """
    Retrieves a variable from the global (root) level.
    
    ### Inputs:
    - Flow (flow): Trigger the retrieval.
    - Var Name (string): The name of the variable.
    
    ### Outputs:
    - Flow (flow): Pulse triggered after retrieval.
    - Value (any): The current value of the global variable.
    """
    version = "2.1.0"

    def __init__(self, node_id, name, bridge):
        super().__init__(node_id, name, bridge)
        self.is_native = True
        self.properties["Var Name"] = ""
        self.define_schema()
        self.register_handlers()

    def register_handlers(self):
        self.register_handler("Flow", self.do_work)

    def define_schema(self):
        self.input_schema = {
            "Flow": DataType.FLOW,
            "Var Name": DataType.STRING
        }
        self.output_schema = {
            "Flow": DataType.FLOW,
            "Value": DataType.ANY
        }

    def do_work(self, **kwargs):
        name = kwargs.get("Var Name") or self.properties.get("Var Name")
        
        if not name:
            self.logger.warning("Global Var Get: No variable name provided.")
            self.set_output("Value", None)
            self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
            return True

        val = self.bridge.get(name, scope_id="Global")
        self.set_output("Value", val)
        self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
        return True

