import google.generativeai as genai
from typing import Dict, List, Any, Optional
import json

from app.llm.base import LLMProvider
from app.core.config import settings

class GeminiProvider(LLMProvider):
    """Google Gemini implementation of LLM provider."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        
    async def generate_text(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """Generate text using Gemini."""
        options = options or {}
        
        model_name = options.get("model", "gemini-1.5-pro")
        temperature = options.get("temperature", 0.7)
        max_tokens = options.get("max_tokens", 1000)
        
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
            return response.text
        except Exception as e:
            print(f"Error generating text with Gemini: {e}")
            return f"Error: {str(e)}"
    
    async def generate_image(self, prompt: str, options: Dict[str, Any] = None) -> str:
        """Generate image using Gemini's image generation capabilities."""
        options = options or {}
        
        try:
            # Note: This is a placeholder as Gemini's image generation API might change
            # Adjust implementation based on the latest Gemini API documentation
            model = genai.GenerativeModel(model_name="gemini-1.5-pro-vision")
            response = model.generate_content(
                [prompt, "Generate an image based on this description."],
                generation_config=genai.GenerationConfig(
                    temperature=0.7
                )
            )
            # This is a placeholder - actual implementation would depend on how Gemini returns image URLs
            return "Image generation with Gemini is not fully implemented yet."
        except Exception as e:
            print(f"Error generating image with Gemini: {e}")
            return f"Error: {str(e)}"
    
    async def search_web(self, query: str, options: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search web using Gemini's web search capabilities."""
        options = options or {}
        
        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-pro")
            response = model.generate_content(
                f"""
                Search the web for: {query}
                
                Return the search results as a JSON array of objects with the following structure:
                [
                    {{
                        "title": "Result title",
                        "url": "Result URL",
                        "snippet": "Brief description or snippet from the result"
                    }}
                ]
                
                Return only the JSON array, nothing else.
                """,
                generation_config=genai.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=2000
                )
            )
            
            # Extract JSON from response
            content = response.text
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return []
        except Exception as e:
            print(f"Error searching web with Gemini: {e}")
            return []
    
    async def analyze_competitor(self, url: str, analysis_type: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze competitor content using Gemini."""
        options = options or {}
        
        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-pro")
            response = model.generate_content(
                f"""
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
                
                Return only the JSON object, nothing else.
                """,
                generation_config=genai.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=2000
                )
            )
            
            # Extract JSON from response
            content = response.text
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise json.JSONDecodeError("No JSON found", content, 0)
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
        
        num_ideas = options.get("num_ideas", 5)
        
        # Convert analysis data to string for prompt
        analysis_str = json.dumps(analysis_data, indent=2)
        
        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-pro")
            response = model.generate_content(
                f"""
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
                
                Return only the JSON array, nothing else.
                """,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2000
                )
            )
            
            # Extract JSON from response
            content = response.text
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                raise json.JSONDecodeError("No JSON found", content, 0)
        except json.JSONDecodeError:
            # Fallback if response is not valid JSON
            return [{"prompt_text": "Error generating prompt ideas", "confidence_score": 0, "explanation": "Error parsing response"}]
