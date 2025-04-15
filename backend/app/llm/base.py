from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def generate_text(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """Generate text based on prompt."""
        pass
    
    @abstractmethod
    async def generate_image(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """Generate image based on prompt and return URL."""
        pass
    
    @abstractmethod
    async def search_web(self, query: str, options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search web for information."""
        pass
    
    @abstractmethod
    async def analyze_competitor(self, url: str, analysis_type: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze competitor content."""
        pass
    
    @abstractmethod
    async def generate_prompt_ideas(self, analysis_data: Dict[str, Any], options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate prompt ideas based on analysis data."""
        pass
