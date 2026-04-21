from app.config.connection import Session as SessionGenerator
from sqlalchemy.orm import Session


def get_db():
    session = SessionGenerator()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
