import os

DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:pass@db/adastra")
