from cryptography.fernet import Fernet
from app.core.config import settings
import base64
import hashlib

class ConfigurationService:
    """Service for managing API keys and configurations."""
    
    def __init__(self):
        # Generate a key from the secret key
        key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
        # Convert to URL-safe base64-encoded key
        self.key = base64.urlsafe_b64encode(key)
        self.cipher = Fernet(self.key)
    
    def encrypt_api_key(self, api_key: str) -> str:
        """Encrypt an API key."""
        return self.cipher.encrypt(api_key.encode()).decode()
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Decrypt an API key."""
        return self.cipher.decrypt(encrypted_key.encode()).decode()
    
    def get_api_key(self, provider: str, db) -> str:
        """Get API key for a provider from the database."""
        from app.models.models import ApiKey
        
        api_key = db.query(ApiKey).filter(ApiKey.provider == provider, ApiKey.is_active == True).first()
        if not api_key:
            raise ValueError(f"No active API key found for provider: {provider}")
        
        return self.decrypt_api_key(api_key.encrypted_key)
    
    def get_configuration(self, key: str, db) -> str:
        """Get configuration value from the database."""
        from app.models.models import Configuration
        
        config = db.query(Configuration).filter(Configuration.key == key).first()
        if not config:
            raise ValueError(f"Configuration not found: {key}")
        
        return config.value
