import os
import json
import uuid
import base64
import hashlib
from typing import Dict, Optional
from axonpulse.utils.logger import setup_logger

logger = setup_logger("Vault")

class VaultManager:
    """
    Manages securely encrypted secrets stored locally on the machine.
    Uses a machine-derived key to encrypt and decrypt the vault.json file
    in the user's ~/.axonpulse directory.
    """
    def __init__(self):
        self.vault_dir = os.path.join(os.path.expanduser("~"), ".axonpulse")
        self.vault_file = os.path.join(self.vault_dir, "vault.json")
        self._key = self._derive_machine_key()
        self._cache: Dict[str, str] = {}
        self._load()

    def _derive_machine_key(self) -> bytes:
        """
        Derives a machine-specific symmetric key based on MAC address.
        This provides basic local-only security, meaning the vault file cannot 
        be merely copied to another machine to extract secrets.
        """
        mac = uuid.getnode()
        # Create a SHA256 hash of the MAC address to use as our 32-byte key
        key_hash = hashlib.sha256(str(mac).encode('utf-8')).digest()
        return key_hash

    def _encrypt(self, text: str) -> str:
        """Simple XOR encryption using the machine key."""
        text_bytes = text.encode('utf-8')
        key_len = len(self._key)
        encrypted = bytearray()
        
        for i, byte in enumerate(text_bytes):
            key_byte = self._key[i % key_len]
            encrypted.append(byte ^ key_byte)
            
        return base64.b64encode(encrypted).decode('utf-8')

    def _decrypt(self, cipher_text: str) -> str:
        """Decrypts the XOR encoded text."""
        try:
            cipher_bytes = base64.b64decode(cipher_text)
            key_len = len(self._key)
            decrypted = bytearray()
            
            for i, byte in enumerate(cipher_bytes):
                key_byte = self._key[i % key_len]
                decrypted.append(byte ^ key_byte)
                
            return decrypted.decode('utf-8')
        except Exception as e:
            logger.error(f"Vault decryption failed: {e}")
            return ""

    def _load(self):
        """Loads and decrypts the vault into memory."""
        if not os.path.exists(self.vault_dir):
            os.makedirs(self.vault_dir, exist_ok=True)
            
        if not os.path.exists(self.vault_file):
            self._save()
            return
            
        try:
            with open(self.vault_file, 'r') as f:
                encrypted_data = json.load(f)
                
            for key, cipher_text in encrypted_data.items():
                self._cache[key] = self._decrypt(cipher_text)
                
            logger.info(f"Loaded {len(self._cache)} secrets from Vault.")
        except Exception as e:
            logger.error(f"Failed to load Vault: {e}")
            self._cache = {}

    def _save(self):
        """Encrypts and saves the current cache to disk."""
        try:
            encrypted_data = {}
            for key, plain_text in self._cache.items():
                encrypted_data[key] = self._encrypt(plain_text)
                
            with open(self.vault_file, 'w') as f:
                json.dump(encrypted_data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save Vault to disk: {e}")

    def set_secret(self, key: str, value: str):
        """Sets a secret in the vault."""
        if not key or not value:
            return
        self._cache[key] = value
        self._save()

    def get_secret(self, key: str) -> Optional[str]:
        """Gets a decrypted secret from the vault."""
        return self._cache.get(key)
        
    def delete_secret(self, key: str):
        """Removes a secret from the vault."""
        if key in self._cache:
            del self._cache[key]
            self._save()
            
    def list_keys(self) -> list:
        """Returns a list of all secret keys in the vault."""
        return list(self._cache.keys())

# Create Singleton Instance
vault = VaultManager()
