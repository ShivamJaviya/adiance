from typing import Dict, List, Any, Optional
from app.llm.base import LLMProvider
from app.llm.openai_provider import OpenAIProvider
from app.llm.claude_provider import ClaudeProvider
from app.llm.gemini_provider import GeminiProvider
from app.llm.deepseek_provider import DeepSeekProvider
from app.llm.manus_provider import ManusProvider

class LLMFactory:
    """Factory class for creating LLM provider instances."""
    
    @staticmethod
    def get_provider(provider_name: str, api_key: Optional[str] = None) -> LLMProvider:
        """
        Get an LLM provider instance based on the provider name.
        
        Args:
            provider_name: Name of the LLM provider
            api_key: Optional API key (if not provided, will use from settings)
            
        Returns:
            An instance of the specified LLM provider
        """
        provider_map = {
            "openai": OpenAIProvider,
            "claude": ClaudeProvider,
            "gemini": GeminiProvider,
            "deepseek": DeepSeekProvider,
            "manus": ManusProvider
        }
        
        if provider_name.lower() not in provider_map:
            raise ValueError(f"Unsupported provider: {provider_name}")
        
        provider_class = provider_map[provider_name.lower()]
        return provider_class(api_key=api_key)
