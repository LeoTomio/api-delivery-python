from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from models import db, User
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from jose import jwt, JWTError


def get_session():
    try:
        Session = sessionmaker(db)
        session = Session()
        yield session
    finally:
        session.close()


def token_verifier(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(decoded_token.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
    
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return user
