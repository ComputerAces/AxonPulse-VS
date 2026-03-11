from axonpulse.core.super_node import SuperNode
from axonpulse.nodes.registry import NodeRegistry
from axonpulse.core.types import DataType
from axonpulse.utils.vault import vault

@NodeRegistry.register("Vault Set", "Workflow/Variables")
class VaultSetNode(SuperNode):
    """
    Encrypts and stores a secret in the local machine's Enterprise Vault.
    The secret is tied to this machine and will not be exported in the .syp JSON payload.
    
    ### Inputs:
    - Flow (flow): Trigger the store action.
    - Key (string): The alias/name for the secret (e.g., 'OPENAI_API_KEY').
    - Secret (string): The plain text secret value to encrypt.
    
    ### Outputs:
    - Flow (flow): Pulse triggered after the secret is stored securely.
    """
    version = "2.1.0"

    def __init__(self, node_id, name, bridge):
        super().__init__(node_id, name, bridge)
        self.is_native = True
        self.properties["Key"] = ""
        self.properties["Secret"] = ""
        self.define_schema()
        self.register_handlers()

    def register_handlers(self):
        self.register_handler("Flow", self.do_work)

    def define_schema(self):
        self.input_schema = {
            "Flow": DataType.FLOW,
            "Key": DataType.STRING,
            "Secret": DataType.STRING
        }
        self.output_schema = {
            "Flow": DataType.FLOW
        }

    def do_work(self, **kwargs):
        key = kwargs.get("Key") or self.properties.get("Key")
        secret = kwargs.get("Secret") or self.properties.get("Secret")
        
        if not key or not secret:
            self.logger.warning("Vault Set: Missing Key or Secret. Skipping.")
            self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
            return True

        # Store in the Vault
        vault.set_secret(key, secret)
        self.logger.info(f"Secret securely stored in Vault under alias '{key}'.")
        self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
        return True

@NodeRegistry.register("Vault Get", "Workflow/Variables")
class VaultGetNode(SuperNode):
    """
    Retrieves and decrypts a secret from the local machine's Enterprise Vault.
    
    ### Inputs:
    - Flow (flow): Trigger the retrieval action.
    - Key (string): The alias/name for the secret used during Vault Set.
    
    ### Outputs:
    - Flow (flow): Pulse triggered after retrieval.
    - Value (string): The decrypted String payload, ready to be wired into API Providers.
    """
    version = "2.1.0"

    def __init__(self, node_id, name, bridge):
        super().__init__(node_id, name, bridge)
        self.is_native = True
        self.properties["Key"] = ""
        self.define_schema()
        self.register_handlers()

    def register_handlers(self):
        self.register_handler("Flow", self.do_work)

    def define_schema(self):
        self.input_schema = {
            "Flow": DataType.FLOW,
            "Key": DataType.STRING
        }
        self.output_schema = {
            "Flow": DataType.FLOW,
            "Value": DataType.STRING
        }

    def do_work(self, **kwargs):
        key = kwargs.get("Key") or self.properties.get("Key")
        
        if not key:
            self.logger.warning("Vault Get: Missing Key. Cannot retrieve secret.")
            self.set_output("Value", None)
            self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
            return True

        # Retrieve from Vault
        secret = vault.get_secret(key)
        
        if secret is None:
             self.logger.warning(f"Vault Get: Secret '{key}' not found in the local Vault.")
             self.set_output("Value", None)
        else:
             self.set_output("Value", secret)
             
        self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
        return True
