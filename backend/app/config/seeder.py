import logging
from app.config.connection import Session as SessionGenerator
from typing import List
from .seeds import *

LOGGER = logging.getLogger(__name__)


def seedTable(datas: List):
    session = SessionGenerator()
    try:
        [session.merge(data) for data in datas]
        session.commit()
    except Exception as e:
        LOGGER.error(repr(e))
        session.rollback()
    finally:
        session.close()


def runSeeder():
    seedTable(users)
