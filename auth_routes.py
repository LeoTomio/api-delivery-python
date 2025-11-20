from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.get("/")
async def authentication():
    """
    Rota para fazer o login no sistema
    """
    return {"message": "Rota de autenticação", "authentication": False}
