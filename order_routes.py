from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["Order"])

@order_router.get("/")
async def list():
    """
    Rota para listar os pedidos
    """
    return {"message": "Listagem"}

@order_router.post("/")
async def create():
    """
    Rota para criar novos pedidos
    """
    return {"message": "Criação"}

@order_router.put("/")
async def update():
    """
    Rota para criar editar pedidos
    """
    return {"message": "Edição"}

@order_router.delete("/")
async def delete():
    """
    Rota para criar deletar pedidos
    """
    return {"message": "Remoção"}