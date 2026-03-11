import os
import requests
import zipfile
import logging
from tqdm import tqdm

logger = logging.getLogger("STTUtils")

def download_model(url, dest_path):
    """Downloads a file with a progress bar."""
    if os.path.exists(dest_path):
        return True
        
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(dest_path, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
        return True
    except Exception as e:
        logger.error(f"Failed to download model from {url}: {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)
        return False

def ensure_vosk_model(model_name="vosk-model-small-en-us-0.15"):
    """
    Ensures the specified Vosk model is downloaded and extracted.
    Returns the path to the model directory.
    """
    models_dir = os.path.join(os.path.expanduser("~"), ".axonpulse", "models", "vosk")
    model_path = os.path.join(models_dir, model_name)
    
    if os.path.exists(model_path):
        return model_path
        
    os.makedirs(models_dir, exist_ok=True)
    
    url = f"https://alphacephei.com/vosk/models/{model_name}.zip"
    zip_path = os.path.join(models_dir, f"{model_name}.zip")
    
    print(f"Downloading Vosk model: {model_name}...")
    if download_model(url, zip_path):
        print(f"Extracting {model_name}...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(models_dir)
            os.remove(zip_path)
            return model_path
        except Exception as e:
            logger.error(f"Failed to extract Vosk model: {e}")
            if os.path.exists(zip_path): os.remove(zip_path)
            return None
    return None
