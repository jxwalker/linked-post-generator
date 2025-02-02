import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import SessionLocal
from src.models.user import User
from src.core.auth import get_password_hash

def create_superuser(email: str, password: str):
    db = SessionLocal()
    try:
        # Check if user exists
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
    if len(sys.argv) != 3:
        print("Usage: python create_superuser.py email password")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    create_superuser(email, password) 