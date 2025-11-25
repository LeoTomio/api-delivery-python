from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session
from schemas import OrderSchema, OrderItemsSchema
from models import Order, User, OrderItems
from auth_routes import token_verifier

order_router = APIRouter(prefix="/orders", tags=["Order"], dependencies=[Depends(token_verifier)])


@order_router.post("/")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    """
    Rota para criar novos pedidos
    """
    newOrder = Order(user=order_schema.user)
    session.add(newOrder)
    session.commit()
    return {"message": "Pedido criado com sucesso"}


@order_router.post("/order/cancel/{id_order}")
async def cancel_order(id_order: int, session: Session = Depends(get_session), user: User = Depends(token_verifier)):
    order = session.query(Order).filter(Order.id == id_order).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")

    if not user.is_admin and order.user != user.id:
        raise HTTPException(status_code=400, detail="Você não tem permissão para cancelar esse pedido")

    order.status = "CANCELED"
    session.commit()
    return {"message": f"Pedido {order.id} cancelado com sucesso", "order": order}


@order_router.get("/")
async def list(session: Session = Depends(get_session), user: User = Depends(token_verifier)):
    """
    Rota para listar os pedidos, necessário autenticação
    """
    if not user.is_admin:
        raise HTTPException(status_code=401, detail=" Vocês não tem permissão para listar os pedidos")
    else:
        order_list = session.query(Order).all()

    return {"orders": order_list}


@order_router.post("/order/add-item/{order_id}")
async def add_order_item(order_id: int, order_items_schema: OrderItemsSchema, session: Session = Depends(get_session), user: User = Depends(token_verifier)):
    """
    Rota para criar editar pedidos
    """
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não existente")
    elif not user.is_admin and order.user != user.id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa operação pedido")
    elif not order.status == "PENDDING":
        raise HTTPException(status_code=400, detail="Pedido está cancelado ou fechado")
    order_item = OrderItems(order_items_schema.quantity, order_items_schema.flavor, order_items_schema.size, order_items_schema.price, order.id)
    session.add(order_item)
    order.price_calculator()
    session.commit()

    return {"message": "Item adicionado com sucesso", "order_item": order_item.id, "order": order.price}


@order_router.put("/order")
async def update(session: Session = Depends(get_session), user: User = Depends(token_verifier)):
    """
    Rota para criar editar pedidos
    """
    return {"message": "Edição"}


@order_router.delete("/")
async def delete(session: Session = Depends(get_session)):
    """
    Rota para criar deletar pedidos
    """

    session.query(User).delete()
    session.commit()
    return {"message": "Remoção"}
