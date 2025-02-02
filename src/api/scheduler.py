from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.core.scheduler import PostScheduler
from src.core.auth import get_current_active_user
from src.database import get_db
from src.models.user import User
from pydantic import BaseModel

router = APIRouter()
scheduler = PostScheduler()

class ScheduleRequest(BaseModel):
    sources: List[str]
    platforms: List[str]
    schedule: str  # Cron expression
    notify_email: str = None

class ScheduleResponse(BaseModel):
    job_id: str
    next_run_time: str
    trigger: str

@router.post("/schedules", response_model=ScheduleResponse)
async def create_schedule(
    request: ScheduleRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new post generation schedule"""
    try:
        job_id = await scheduler.schedule_post_generation(
            current_user.id,
            request.sources,
            request.platforms,
            request.schedule,
            request.notify_email
        )
        
        job = scheduler.scheduler.get_job(job_id)
        return {
            "job_id": job_id,
            "next_run_time": str(job.next_run_time),
            "trigger": str(job.trigger)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/schedules", response_model=List[ScheduleResponse])
async def get_schedules(current_user: User = Depends(get_current_active_user)):
    """Get all schedules for current user"""
    schedules = scheduler.get_user_schedules(current_user.id)
    return schedules

@router.delete("/schedules/{job_id}")
async def delete_schedule(
    job_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a schedule"""
    if not job_id.startswith(f"user_{current_user.id}_"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this schedule"
        )
    
    try:
        scheduler.remove_schedule(job_id)
        return {"message": "Schedule deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 