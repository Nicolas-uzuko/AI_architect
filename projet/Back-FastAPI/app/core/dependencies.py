"""
Dépendances FastAPI (Injection).
"""
import logging
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.user import User

logger = logging.getLogger(__name__)

async def get_current_user(db: AsyncSession = Depends(get_db)) -> User:
    """
    Simule un utilisateur connecté (Dummy User).
    Crée l'utilisateur par défaut s'il n'existe pas en base de données.
    À remplacer plus tard par une vraie authentification JWT.
    """
    dummy_email = "dummy@example.com"
    stmt = select(User).where(User.email == dummy_email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            name="Dummy User",
            email=dummy_email,
            password_hash="fake_hash_for_now",
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Faux utilisateur créé : {user.id}")
        
    return user
