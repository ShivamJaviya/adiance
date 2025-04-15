from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base

class ApiKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, unique=True, index=True)
    encrypted_key = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Configuration(Base):
    __tablename__ = "configurations"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class CompetitorAnalysis(Base):
    __tablename__ = "competitor_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    competitor_url = Column(String)
    analysis_type = Column(String)  # blog, social, website
    provider = Column(String)  # LLM provider used
    content_themes = Column(Text)
    content_strategy = Column(Text)
    raw_analysis = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    prompt_ideas = relationship("PromptIdea", back_populates="analysis")

class PromptIdea(Base):
    __tablename__ = "prompt_ideas"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("competitor_analyses.id"))
    prompt_text = Column(Text)
    provider = Column(String)  # LLM provider used
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    analysis = relationship("CompetitorAnalysis", back_populates="prompt_ideas")
    generated_contents = relationship("GeneratedContent", back_populates="prompt")

class GeneratedContent(Base):
    __tablename__ = "generated_contents"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompt_ideas.id"))
    content_type = Column(String)  # text, image, video, text+image
    content_text = Column(Text, nullable=True)
    content_url = Column(String, nullable=True)  # For images/videos
    provider = Column(String)  # LLM provider used
    parameters = Column(Text, nullable=True)  # JSON string of parameters used
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    prompt = relationship("PromptIdea", back_populates="generated_contents")
