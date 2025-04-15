import os
import openai
from typing import Dict, List, Any, Optional
import json

from app.llm.base import LLMProvider
from app.core.config import settings

class OpenAIProvider(LLMProvider):
    """OpenAI implementation of LLM provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        openai.api_key = self.api_key
        
    async def generate_text(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """Generate text using OpenAI."""
        options = options or {}
        
        model = options.get("model", "gpt-4")
        temperature = options.get("temperature", 0.7)
        max_tokens = options.get("max_tokens", 1000)
        
        try:
            response = await openai.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating text with OpenAI: {e}")
            return f"Error: {str(e)}"
    
    async def generate_image(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """Generate image using DALL-E and return URL."""
        options = options or {}
        
        size = options.get("size", "1024x1024")
        quality = options.get("quality", "standard")
        
        try:
            response = await openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=1
            )
            return response.data[0].url
        except Exception as e:
            print(f"Error generating image with OpenAI: {e}")
            return f"Error: {str(e)}"
    
    async def search_web(self, query: str, options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search web using OpenAI's web search capability."""
        options = options or {}
        
        model = options.get("model", "gpt-4")
        
        try:
            # Using GPT-4 with web browsing capability
            response = await openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant with web search capabilities. Search the web for the latest information and return results in JSON format."},
                    {"role": "user", "content": f"Search the web for: {query}. Return results as a JSON array of objects with 'title', 'url', and 'snippet' fields."}
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get("results", [])
        except Exception as e:
            print(f"Error searching web with OpenAI: {e}")
            return []
    
    async def analyze_competitor(self, url: str, analysis_type: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze competitor content using OpenAI."""
        options = options or {}
        
        model = options.get("model", "gpt-4")
        
        prompt = f"""
        Analyze the competitor content at {url}. Focus on {analysis_type} content.
        
        Provide a detailed analysis including:
        1. Main content themes
        2. Content strategy observations
        3. Tone and style analysis
        4. Target audience insights
        5. Content gaps or opportunities
        
        Format your response as a JSON object with the following structure:
        {{
            "content_themes": [list of main themes with confidence scores],
            "content_strategy": [list of strategy observations],
            "tone_analysis": string description,
            "target_audience": string description,
            "opportunities": [list of content opportunities]
        }}
        """
        
        try:
            response = await self.generate_text(prompt, {"model": model, "max_tokens": 2000})
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback if response is not valid JSON
            return {
                "content_themes": ["Error parsing response"],
                "content_strategy": ["Error parsing response"],
                "tone_analysis": "Error parsing response",
                "target_audience": "Error parsing response",
                "opportunities": ["Error parsing response"]
            }
    
    async def generate_prompt_ideas(self, analysis_data: Dict[str, Any], options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate prompt ideas based on analysis data."""
        options = options or {}
        
        model = options.get("model", "gpt-4")
        num_ideas = options.get("num_ideas", 5)
        
        # Convert analysis data to string for prompt
        analysis_str = json.dumps(analysis_data, indent=2)
        
        prompt = f"""
        Based on the following competitor analysis, generate {num_ideas} creative prompt ideas for marketing content:
        
        {analysis_str}
        
        For each prompt idea:
        1. Create a compelling prompt that would generate excellent marketing content
        2. Assign a confidence score (0-100) based on how well it addresses the opportunities
        3. Add a brief explanation of why this prompt would be effective
        
        Format your response as a JSON array of objects with the following structure:
        [
            {{
                "prompt_text": "The complete prompt text",
                "confidence_score": numeric score between 0-100,
                "explanation": "Brief explanation of effectiveness"
            }}
        ]
        """
        
        try:
            response = await self.generate_text(prompt, {"model": model, "max_tokens": 2000})
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback if response is not valid JSON
            return [{"prompt_text": "Error generating prompt ideas", "confidence_score": 0, "explanation": "Error parsing response"}]
