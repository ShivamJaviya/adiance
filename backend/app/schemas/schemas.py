from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# API Key schemas
class ApiKeyBase(BaseModel):
    provider: str
    
class ApiKeyCreate(ApiKeyBase):
    api_key: str
    
class ApiKey(ApiKeyBase):
    id: int
    encrypted_key: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Configuration schemas
class ConfigurationBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None
    
class ConfigurationCreate(ConfigurationBase):
    pass
    
class Configuration(ConfigurationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Competitor Analysis schemas
class CompetitorAnalysisBase(BaseModel):
    competitor_url: str
    analysis_type: str
    
class CompetitorAnalysisRequest(CompetitorAnalysisBase):
    provider: str
    
class CompetitorAnalysisResponse(BaseModel):
    id: int
    competitor_url: str
    analysis_type: str
    provider: str
    content_themes: List[Dict[str, Any]]
    content_strategy: List[str]
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class CompetitorAnalysis(CompetitorAnalysisResponse):
    raw_analysis: str
    
    class Config:
        orm_mode = True

# Prompt Idea schemas
class PromptIdeaBase(BaseModel):
    prompt_text: str
    confidence_score: Optional[float] = None
    
class PromptIdeaRequest(BaseModel):
    analysis_id: int
    provider: str
    num_ideas: Optional[int] = 5
    
class PromptIdea(PromptIdeaBase):
    id: int
    analysis_id: int
    provider: str
    created_at: datetime
    
    class Config:
        orm_mode = True

# Content Generation schemas
class ContentGenerationBase(BaseModel):
    content_type: str
    parameters: Optional[Dict[str, Any]] = None
    
class ContentGenerationRequest(ContentGenerationBase):
    prompt_id: int
    provider: str
    
class GeneratedContentResponse(BaseModel):
    id: int
    prompt_id: int
    content_type: str
    content_text: Optional[str] = None
    content_url: Optional[str] = None
    provider: str
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class GeneratedContent(GeneratedContentResponse):
    parameters: Optional[str] = None
    
    class Config:
        orm_mode = True
