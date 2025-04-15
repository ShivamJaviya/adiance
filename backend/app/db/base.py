from app.models import models
from app.db.session import Base

# Import all models here to ensure they are registered with SQLAlchemy
# This file is imported in app/main.py to create tables

__all__ = ["models", "Base"]
