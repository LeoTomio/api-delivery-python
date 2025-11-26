from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session
from schemas import OrderSchema, OrderItemsSchema, ResponseOrderSchema
from models import Order, User, OrderItems
from auth_routes import token_verifier
from typing import List

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


@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(token_verifier)):
    """
    Rota paara cancelar pedido
    """
    order = session.query(Order).filter(Order.id == order_id).first()
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
    Rota para listar os pedidos
    """
    if not user.is_admin:
        raise HTTPException(status_code=401, detail=" Vocês não tem permissão para listar os pedidos")
    else:
        order_list = session.query(Order).all()

    return {"orders": order_list}


@order_router.post("/order/add-item/{order_id}")
async def add_order_item(order_id: int, order_items_schema: OrderItemsSchema, session: Session = Depends(get_session), user: User = Depends(token_verifier)):
    """
    Rota para adicionar itens ao pedido
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


@order_router.post("/order/remove-item/{order_item_id}")
async def remove_order_item(order_item_id: int, session: Session = Depends(get_session), user: User = Depends(token_verifier)):
    """
    Rota para remover itens do pedido
    """
    order_item = session.query(OrderItems).filter(OrderItems.id == order_item_id).first()
    order = session.query(Order).filter(Order.id == order_item.order).first()

    if not order_item:
        raise HTTPException(status_code=400, detail="Item no pedido não existente")
    elif not user.is_admin and order_item.user != user.id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa operação pedido")

    session.delete(order_item)
    order.price_calculator()
    session.commit()

    return {"message": "Item removido com sucesso", "order_items_quantity": len(order.order_items), "order_item": order}


@order_router.post("/order/finish/{order_id}")
async def finish_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(token_verifier)):
    """
    Rota para finalizar pedido
    """
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")

    if not user.is_admin and order.user != user.id:
        raise HTTPException(status_code=400, detail="Você não tem permissão para cancelar esse pedido")

    order.status = "FINISHED"
    session.commit()
    return {"message": f"Pedido {order.id} finalizado com sucesso", "order": order}


@order_router.get("/order/{order_id}")
async def get_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(token_verifier)):
    """
    Rota para pegar pedido especifico
    """
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido nao encontrado")

    if not user.is_admin and order.user != user.id:
        raise HTTPException(status_code=400, detail="Você não tem permissão para cancelar esse pedido")

    return {"order_item_quantity": len(order.order_items), "order": order}
    # return order


@order_router.get("/listar", response_model=List[ResponseOrderSchema])
async def list(session: Session = Depends(get_session), user: User = Depends(token_verifier)):
    """
    Rota para listar todos os pedidos de um usuário
    """
    if not user.is_admin:
        raise HTTPException(status_code=401, detail=" Vocês não tem permissão para listar os pedidos")
    else:
        order_list = session.query(Order).filter(Order.user == user.id).all()

    return {"orders": order_list}
