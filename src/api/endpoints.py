from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from src.core.generator import PostGenerator
from src.core.auth import get_current_active_user
from src.database import get_db
from src.models.user import User
from pydantic import BaseModel

router = APIRouter()
generator = PostGenerator()

class GeneratePostRequest(BaseModel):
    sources: List[str]
    platforms: List[str]
    schedule: Optional[str] = None
    notify_email: Optional[str] = None

class PostHistoryItem(BaseModel):
    id: int
    content: str
    platform: str
    created_at: datetime
    status: str

@router.post("/generate", response_model=dict)
async def generate_posts(
    request: GeneratePostRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate posts from news sources"""
    try:
        posts = await generator.generate_posts(request.sources, request.platforms)
        
        # Save generated posts to history
        for platform, content in posts.items():
            post_history = PostHistory(
                user_id=current_user.id,
                content=content,
                platform=platform,
                status="generated"
            )
            db.add(post_history)
        db.commit()
        
        return posts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/posts/history", response_model=List[PostHistoryItem])
async def get_post_history(
    page: int = 1,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's post history"""
    skip = (page - 1) * limit
    posts = db.query(PostHistory)\
        .filter(PostHistory.user_id == current_user.id)\
        .order_by(PostHistory.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return posts

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a post from history"""
    post = db.query(PostHistory)\
        .filter(PostHistory.id == post_id, PostHistory.user_id == current_user.id)\
        .first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

@router.get("/health")
async def health_check():
    """API health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()} 