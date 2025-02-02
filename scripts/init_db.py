import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Base, engine, SessionLocal
from src.models.user import User
from src.models.post import PostHistory
from src.core.auth import get_password_hash

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

def create_superuser(email: str, password: str):
    db = SessionLocal()
    try:
        # Check if superuser exists
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"User {email} already exists")
            return

        # Create superuser
        superuser = User(
            email=email,
            hashed_password=get_password_hash(password),
            is_superuser=True
        )
        db.add(superuser)
        db.commit()
        print(f"Superuser {email} created successfully")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    
    if len(sys.argv) == 3:
        email = sys.argv[1]
        password = sys.argv[2]
        create_superuser(email, password)
    else:
        print("To create a superuser, run: python init_db.py email password") 