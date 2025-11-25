from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from schemas import OrderSchema
from models import Order

order_router = APIRouter(prefix="/order", tags=["Order"])


@order_router.get("/")
async def list():
    """
    Rota para listar os pedidos, necessário autenticação
    """
    return {"message": "Listagem"}


@order_router.post("/")
async def create_order(
    order_schema: OrderSchema, session: Session = Depends(get_session)
):
    """
    Rota para criar novos pedidos
    """
    newOrder = Order(user=order_schema.user)
    session.add(newOrder)
    session.commit()
    return {"message": "Pedido criado com sucesso"}


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
