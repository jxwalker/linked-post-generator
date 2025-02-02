from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from datetime import datetime
from src.core.generator import PostGenerator
from src.utils.emailer import EmailNotifier
from src.models.post import PostHistory
from src.database import SessionLocal

class PostScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.generator = PostGenerator()
        self.notifier = EmailNotifier()
    
    async def schedule_post_generation(
        self,
        user_id: int,
        sources: list,
        platforms: list,
        schedule: str,  # Cron expression
        notify_email: str = None
    ):
        """Schedule periodic post generation for a user"""
        
        async def generate_and_notify():
            db = SessionLocal()
            try:
                # Generate posts
                posts = await self.generator.generate_posts(sources, platforms)
                
                # Save to history
                for platform, content in posts.items():
                    post_history = PostHistory(
                        user_id=user_id,
                        content=content,
                        platform=platform,
                        status="scheduled"
                    )
                    db.add(post_history)
                db.commit()
                
                # Send notification if email provided
                if notify_email:
                    await self.notifier.send_notification(
                        notify_email,
                        "Scheduled Posts Generated",
                        f"Generated {len(posts)} posts for platforms: {', '.join(platforms)}"
                    )
                    
                return posts
                
            except Exception as e:
                if notify_email:
                    await self.notifier.send_notification(
                        notify_email,
                        "Scheduled Post Generation Failed",
                        str(e)
                    )
                raise
            finally:
                db.close()
        
        # Add job to scheduler
        job = self.scheduler.add_job(
            generate_and_notify,
            CronTrigger.from_crontab(schedule),
            id=f"user_{user_id}_{datetime.now().timestamp()}",
            replace_existing=True
        )
        
        return job.id
    
    def remove_schedule(self, job_id: str):
        """Remove a scheduled job"""
        self.scheduler.remove_job(job_id)
    
    def get_user_schedules(self, user_id: int):
        """Get all scheduled jobs for a user"""
        jobs = []
        for job in self.scheduler.get_jobs():
            if job.id.startswith(f"user_{user_id}_"):
                jobs.append({
                    'id': job.id,
                    'next_run_time': job.next_run_time,
                    'trigger': str(job.trigger)
                })
        return jobs
    
    def start(self):
        """Start the scheduler"""
        self.scheduler.start()
    
    def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown() 