from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.services.config_service import ConfigurationService

router = APIRouter()
config_service = ConfigurationService()

@router.get("/api-keys", response_model=List[schemas.ApiKey])
async def get_api_keys(db: Session = Depends(get_db)):
    """Get all API keys."""
    api_keys = db.query(models.ApiKey).all()
    return api_keys

@router.post("/api-keys", response_model=schemas.ApiKey)
async def create_api_key(api_key: schemas.ApiKeyCreate, db: Session = Depends(get_db)):
    """Create a new API key."""
    # Check if provider already exists
    existing_key = db.query(models.ApiKey).filter(models.ApiKey.provider == api_key.provider).first()
    if existing_key:
        # Update existing key
        encrypted_key = config_service.encrypt_api_key(api_key.api_key)
        existing_key.encrypted_key = encrypted_key
        existing_key.is_active = True
        db.commit()
        db.refresh(existing_key)
        return existing_key
    
    # Create new key
    encrypted_key = config_service.encrypt_api_key(api_key.api_key)
    db_api_key = models.ApiKey(
        provider=api_key.provider,
        encrypted_key=encrypted_key,
        is_active=True
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return db_api_key

@router.delete("/api-keys/{provider}", response_model=schemas.ApiKey)
async def delete_api_key(provider: str, db: Session = Depends(get_db)):
    """Delete an API key."""
    api_key = db.query(models.ApiKey).filter(models.ApiKey.provider == provider).first()
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    api_key.is_active = False
    db.commit()
    db.refresh(api_key)
    return api_key

@router.get("/configurations", response_model=List[schemas.Configuration])
async def get_configurations(db: Session = Depends(get_db)):
    """Get all configurations."""
    configurations = db.query(models.Configuration).all()
    return configurations

@router.post("/configurations", response_model=schemas.Configuration)
async def create_configuration(config: schemas.ConfigurationCreate, db: Session = Depends(get_db)):
    """Create a new configuration."""
    # Check if key already exists
    existing_config = db.query(models.Configuration).filter(models.Configuration.key == config.key).first()
    if existing_config:
        # Update existing config
        existing_config.value = config.value
        existing_config.description = config.description
        db.commit()
        db.refresh(existing_config)
        return existing_config
    
    # Create new config
    db_config = models.Configuration(
        key=config.key,
        value=config.value,
        description=config.description
    )
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config
