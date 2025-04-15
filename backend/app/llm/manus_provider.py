import httpx
from typing import Dict, List, Any, Optional
import json

from app.llm.base import LLMProvider
from app.core.config import settings

class ManusProvider(LLMProvider):
    """Manus implementation of LLM provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.MANUS_API_KEY
        self.api_url = "https://api.manus.ai/v1"  # Placeholder API endpoint
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    async def generate_text(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """Generate text using Manus."""
        options = options or {}
        
        model = options.get("model", "manus-default")
        temperature = options.get("temperature", 0.7)
        max_tokens = options.get("max_tokens", 1000)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/completions",
                    headers=self.headers,
                    json={
                        "model": model,
                        "prompt": prompt,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("text", "")
                else:
                    return f"Error: API returned status code {response.status_code}"
        except Exception as e:
            print(f"Error generating text with Manus: {e}")
            return f"Error: {str(e)}"
    
    async def generate_image(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """Generate image using Manus."""
        options = options or {}
        
        size = options.get("size", "1024x1024")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/images/generate",
                    headers=self.headers,
                    json={
                        "prompt": prompt,
                        "size": size
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("image_url", "")
                else:
                    return f"Error: API returned status code {response.status_code}"
        except Exception as e:
            print(f"Error generating image with Manus: {e}")
            return f"Error: {str(e)}"
    
    async def search_web(self, query: str, options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search web using Manus's capabilities."""
        options = options or {}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/search",
                    headers=self.headers,
                    json={
                        "query": query
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("results", [])
                else:
                    print(f"Error searching web with Manus: API returned status code {response.status_code}")
                    return []
        except Exception as e:
            print(f"Error searching web with Manus: {e}")
            return []
    
    async def analyze_competitor(self, url: str, analysis_type: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze competitor content using Manus."""
        options = options or {}
        
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
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/analyze",
                    headers=self.headers,
                    json={
                        "url": url,
                        "analysis_type": analysis_type,
                        "prompt": prompt
                    },
                    timeout=120.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    # Fallback to text generation if direct analysis fails
                    text_response = await self.generate_text(prompt)
                    try:
                        # Extract JSON from response
                        start_idx = text_response.find('{')
                        end_idx = text_response.rfind('}') + 1
                        
                        if start_idx >= 0 and end_idx > start_idx:
                            json_str = text_response[start_idx:end_idx]
                            return json.loads(json_str)
                        else:
                            raise json.JSONDecodeError("No JSON found", text_response, 0)
                    except json.JSONDecodeError:
                        return {
                            "content_themes": ["Error parsing response"],
                            "content_strategy": ["Error parsing response"],
                            "tone_analysis": "Error parsing response",
                            "target_audience": "Error parsing response",
                            "opportunities": ["Error parsing response"]
                        }
        except Exception as e:
            print(f"Error analyzing competitor with Manus: {e}")
            return {
                "content_themes": [f"Error: {str(e)}"],
                "content_strategy": ["Error occurred during analysis"],
                "tone_analysis": "Error occurred during analysis",
                "target_audience": "Error occurred during analysis",
                "opportunities": ["Error occurred during analysis"]
            }
    
    async def generate_prompt_ideas(self, analysis_data: Dict[str, Any], options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate prompt ideas based on analysis data."""
        options = options or {}
        
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
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/generate_prompts",
                    headers=self.headers,
                    json={
                        "analysis": analysis_data,
                        "num_ideas": num_ideas
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    return response.json().get("prompt_ideas", [])
                else:
                    # Fallback to text generation if direct prompt generation fails
                    text_response = await self.generate_text(prompt)
                    try:
                        # Extract JSON from response
                        start_idx = text_response.find('[')
                        end_idx = text_response.rfind(']') + 1
                        
                        if start_idx >= 0 and end_idx > start_idx:
                            json_str = text_response[start_idx:end_idx]
                            return json.loads(json_str)
                        else:
                            raise json.JSONDecodeError("No JSON found", text_response, 0)
                    except json.JSONDecodeError:
                        return [{"prompt_text": "Error generating prompt ideas", "confidence_score": 0, "explanation": "Error parsing response"}]
        except Exception as e:
            print(f"Error generating prompt ideas with Manus: {e}")
            return [{"prompt_text": f"Error: {str(e)}", "confidence_score": 0, "explanation": "Error occurred during generation"}]
