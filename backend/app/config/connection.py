from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_URL = getenv("DB_URL")
if not DB_URL:
    raise Exception("DB_URL environment variable is not set")
engine = create_engine(DB_URL, pool_pre_ping=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
