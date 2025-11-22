from sqlalchemy.orm import sessionmaker
from models import db


def get_session():
    try:
        Session = sessionmaker(db)
        session = Session()
        yield session # como se fosse um return mas sem encerrar a função
    finally:
        session.close()
