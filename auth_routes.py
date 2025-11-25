from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session, token_verifier
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
auth_router = APIRouter(prefix="/auth", tags=["Auth"])


def create_token(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_data = datetime.now(timezone.utc) + token_duration
    dic_info = {"sub": str(user_id), "exp": expiration_data}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def user_autentication(email, password, session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user


@auth_router.get("/")
async def authentication():
    """
    Rota para fazer o login no sistema
    """
    return {"message": "Rota de autenticação", "authentication": False}


@auth_router.post("/")
async def createAccount(user_schema: UserSchema, session: Session = Depends(get_session)):
    """
    Rota para criar uma conta no sistema
    """
    user = session.query(User).filter(User.email == user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Usuário ja cadastrado")
    else:
        hashed_password = bcrypt_context.hash(user_schema.password)
        new_user = User(
            user_schema.name,
            user_schema.email,
            hashed_password,
            user_schema.is_active,
            user_schema.is_active,
        )
        session.add(new_user)
        session.commit()

    return {"message": f"Usuário {user_schema.email} criado com sucesso!"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    """
    Rota de login, onde será gerado o token de autenticação
    """
    user = user_autentication(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
        
@auth_router.post("/login-docs")
async def login_docs(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Rota de login, onde será gerado o token de autenticação
    """
    user = user_autentication(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = create_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }


@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(token_verifier)):
    access_token = create_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
