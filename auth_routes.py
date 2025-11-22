from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.get("/")
async def authentication():
    """
    Rota para fazer o login no sistema
    """
    return {"message": "Rota de autenticação", "authentication": False}


@auth_router.post("/")
async def createAccount(
    userSchema: UserSchema, session: Session = Depends(get_session)
):
    """
    Rota para criar uma conta no sistema
    """
    user = session.query(User).filter(User.email == userSchema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Usuário ja cadastrado")
    else:
        hashed_password = bcrypt_context.hash(userSchema.password)
        new_user = User(userSchema.name, userSchema.email, hashed_password, userSchema.is_active, userSchema.is_active)
        session.add(new_user)
        session.commit()

    return {"message": f"Usuário {userSchema.email} criado com sucesso!"}
