import os

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY',"RUNNING_TEST")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM","HS256")
ACCES_TOKEN_EXPIRE_MINUTES=15



