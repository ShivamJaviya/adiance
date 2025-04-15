import json
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.llm.factory import LLMFactory
from app.models import models
from app.services.config_service import ConfigurationService

class ContentService:
    """Service for generating content based on prompts."""
    
    def __init__(self, db: Session):
        self.db = db
        self.config_service = ConfigurationService()
    
    async def generate_content(
        self, 
        prompt_id: int, 
        content_type: str, 
        provider: str, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate content based on a prompt.
        
        Args:
            prompt_id: ID of the prompt idea
            content_type: Type of content to generate (text, image, video, text+image)
            provider: LLM provider to use
            parameters: Additional parameters for content generation
            
        Returns:
            Generated content
        """
        try:
            # Get prompt
            prompt_idea = self.db.query(models.PromptIdea).filter(models.PromptIdea.id == prompt_id).first()
            if not prompt_idea:
                raise ValueError(f"Prompt idea not found: {prompt_id}")
            
            # Get API key
            api_key = self.config_service.get_api_key(provider, self.db)
            
            # Get LLM provider
            llm_provider = LLMFactory.get_provider(provider, api_key)
            
            # Generate content based on content type
            content_text = None
            content_url = None
            
            if content_type == "text":
                content_text = await llm_provider.generate_text(prompt_idea.prompt_text, parameters)
            elif content_type == "image":
                content_url = await llm_provider.generate_image(prompt_idea.prompt_text, parameters)
            elif content_type == "text+image":
                content_text = await llm_provider.generate_text(prompt_idea.prompt_text, parameters)
                content_url = await llm_provider.generate_image(prompt_idea.prompt_text, parameters)
            elif content_type == "video":
                # Video generation might not be supported by all providers
                content_url = "Video generation not fully implemented yet"
            else:
                raise ValueError(f"Unsupported content type: {content_type}")
            
            # Save to database
            db_content = models.GeneratedContent(
                prompt_id=prompt_id,
                content_type=content_type,
                content_text=content_text,
                content_url=content_url,
                provider=provider,
                parameters=json.dumps(parameters) if parameters else None
            )
            self.db.add(db_content)
            self.db.commit()
            self.db.refresh(db_content)
            
            # Format response
            response = {
                "id": db_content.id,
                "prompt_id": db_content.prompt_id,
                "content_type": db_content.content_type,
                "content_text": db_content.content_text,
                "content_url": db_content.content_url,
                "provider": db_content.provider,
                "created_at": db_content.created_at
            }
            
            return response
        except Exception as e:
            self.db.rollback()
            raise e
