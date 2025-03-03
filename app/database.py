from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import time
from sqlalchemy.exc import OperationalError

# Get database URL from environment variables with fallback
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ecommerce")
# if you're running docker container and want to connect to your local database
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "host.docker.internal")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Add retry logic for database connection
max_retries = 5
retry_delay = 5  # seconds

for retry in range(max_retries):
    try:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_pre_ping=True  # Add connection health check
        )
        # Test the connection
        with engine.connect() as connection:
            break
    except OperationalError as e:
        if retry < max_retries - 1:
            print(f"Database connection attempt {retry + 1} failed. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            raise Exception(f"Could not connect to database after {max_retries} attempts") from e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
