import struct
import math
from axonpulse.core.super_node import SuperNode
from axonpulse.nodes.registry import NodeRegistry
from axonpulse.core.types import DataType

# Lazy Global
pyaudio = None

def ensure_pyaudio():
    global pyaudio
    if pyaudio: return True
    from axonpulse.core.dependencies import DependencyManager
    if DependencyManager.ensure("pyaudio"):
        import pyaudio as _p; pyaudio = _p; return True
    return False

@NodeRegistry.register("Audio Device List", "Media/Audio")
class AudioDeviceListNode(SuperNode):
    """
    Scans the system for available audio input and output devices.
    Returns lists of device names and their corresponding indices.
    
    Outputs:
    - Flow: Triggered after the scan is complete.
    - Input Devices: List of strings (e.g., "0: Microphone").
    - Output Devices: List of strings (e.g., "3: Speakers").
    - Input Count: Number of input devices found.
    - Output Count: Number of output devices found.
    """
    version = "2.1.0"

    def __init__(self, node_id, name, bridge):
        super().__init__(node_id, name, bridge)
        self.is_native = True

    def register_handlers(self):
        super().register_handlers()
        self.register_handler("Flow", self.do_work)

    def define_schema(self):
        self.input_schema = {
            "Flow": DataType.FLOW
        }
        self.output_schema = {
            "Flow": DataType.FLOW,
            "Input Names": DataType.LIST,
            "Input IDs": DataType.LIST,
            "Output Names": DataType.LIST,
            "Output IDs": DataType.LIST,
            "Input Devices": DataType.LIST, # Legacy Support
            "Output Devices": DataType.LIST, # Legacy Support
            "Input Count": DataType.INTEGER,
            "Output Count": DataType.INTEGER
        }

    def do_work(self, **kwargs):
        if not ensure_pyaudio():
            self.logger.error("pyaudio not installed.")
            return False

        self.logger.info("Starting robust audio device scan...")
        p = pyaudio.PyAudio()
        num_devices = p.get_device_count()
        self.logger.info(f"Total devices reported by PyAudio system: {num_devices}")
        
        input_names = []
        input_ids = []
        output_names = []
        output_ids = []
        
        legacy_inputs = []
        legacy_outputs = []
        
        seen_inputs = set()
        seen_outputs = set()
        
        for i in range(num_devices):
            try:
                device_info = p.get_device_info_by_index(i)
                name = device_info.get('name')
                max_in = device_info.get('maxInputChannels', 0)
                max_out = device_info.get('maxOutputChannels', 0)
                
                # Filter for Input
                if max_in > 0:
                    if name not in seen_inputs:
                        input_names.append(name)
                        input_ids.append(i)
                        legacy_inputs.append(f"{i}: {name}")
                        seen_inputs.add(name)
                    
                # Filter for Output
                if max_out > 0:
                    if name not in seen_outputs:
                        output_names.append(name)
                        output_ids.append(i)
                        legacy_outputs.append(f"{i}: {name}")
                        seen_outputs.add(name)
                        
                self.logger.info(f"Device {i}: '{name}' (In: {max_in}, Out: {max_out})")
            except Exception as e:
                self.logger.warning(f"Failed to query audio device {i}: {e}")
                
        p.terminate()
        
        self.logger.info(f"Scan complete. Unique inputs: {len(input_ids)}, Unique outputs: {len(output_ids)}")
        
        # New Granular Outputs
        self.set_output("Input Names", input_names)
        self.set_output("Input IDs", input_ids)
        self.set_output("Output Names", output_names)
        self.set_output("Output IDs", output_ids)
        
        # Legacy Outputs
        self.set_output("Input Devices", legacy_inputs)
        self.set_output("Output Devices", legacy_outputs)
        
        # Counts
        self.set_output("Input Count", len(input_ids))
        self.set_output("Output Count", len(output_ids))
        
        self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
        return True
