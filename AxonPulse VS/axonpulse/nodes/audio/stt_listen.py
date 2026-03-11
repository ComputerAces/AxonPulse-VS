from axonpulse.core.super_node import SuperNode
from axonpulse.nodes.registry import NodeRegistry
from axonpulse.core.types import DataType
import os

@NodeRegistry.register("Listen", "Media/Audio")
class STTListenNode(SuperNode):
    """
    Transcribes audio to text using a registered STT Provider (OS, Vosk, or Whisper).
    
    Acts as a consumer node that sends audio data (WavObject, bytes, or path) 
    to the active STT engine and returns the resulting transcription.
    
    Inputs:
    - Flow: Trigger the transcription.
    - Audio Data: The audio source (WavObject, bytes, or absolute path).
    
    Outputs:
    - Flow: Pulse triggered after transcription completion.
    - Text: The recognized text string.
    """
    version = "2.2.0"

    def __init__(self, node_id, name, bridge):
        super().__init__(node_id, name, bridge)
        self.is_native = True

    def register_handlers(self):
        self.register_handler("Flow", self.do_work)

    def define_schema(self):
        self.input_schema = {
            "Flow": DataType.FLOW,
            "Audio Data": DataType.ANY
        }
        self.output_schema = {
            "Flow": DataType.FLOW,
            "Text": DataType.STRING
        }

    def do_work(self, **kwargs):
        provider = kwargs.get("Provider")
        audio_data = kwargs.get("Audio Data")

        # Auto-discover provider from scope
        if not provider:
            provider_id = self.get_provider_id("STT")
            if provider_id:
                provider = self.bridge.get(f"{provider_id}_Provider")

        if not provider:
            raise RuntimeError(f"[{self.name}] No STT Provider found in scope.")

        if not hasattr(provider, 'transcribe'):
            raise RuntimeError(f"[{self.name}] Provider does not support transcription.")

        if audio_data is None:
            self.logger.warning(f"[{self.name}] No audio data provided.")
            self.bridge.set(f"{self.node_id}_Text", "", self.name)
            self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
            return True

        # Resolve Audio Data
        # Support WavObject (has .filepath), path strings, or raw bytes
        target_audio = audio_data
        if hasattr(audio_data, 'filepath'):
            target_audio = audio_data.filepath
        elif isinstance(audio_data, str):
            # Resolve path just in case
            from axonpulse.utils.path_utils import resolve_project_path
            target_audio = resolve_project_path(audio_data, self.bridge)

        try:
            text = provider.transcribe(target_audio)
            
            self.bridge.set(f"{self.node_id}_Text", text, self.name)
            self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
            return True
        except Exception as e:
            self.logger.error(f"STT Transcription Error: {e}")
            self.bridge.set(f"{self.node_id}_Text", f"Error: {str(e)}", self.name)
            self.bridge.set(f"{self.node_id}_ActivePorts", ["Flow"], self.name)
            return True
