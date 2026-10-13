from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from DataBase import get_session
from models.Order import EstadoPedido, Order
from models.Order_Detail import OrderDetail
from models.Product_Category import Product
from models.Table import Table

router = APIRouter(prefix="/mesero", tags=["Mesero"])


def get_order_or_404(session: Session, order_id: int) -> Order:
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order


def touch(order: Order):
    order.fecha_ultima_actualizacion = datetime.utcnow()


# ---------- Consulta (menú y mesas) ----------
@router.get("/menu", response_model=list[Product])
def get_menu(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()


@router.get("/tables", response_model=list[Table])
def get_tables(session: Session = Depends(get_session)):
    return session.exec(select(Table)).all()


# ---------- CRUD de pedidos ----------
@router.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order: Order, session: Session = Depends(get_session)):
    order.id = None
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.get("/orders", response_model=list[Order])
def list_orders(estado: EstadoPedido | None = None, session: Session = Depends(get_session)):
    query = select(Order)
    if estado:
        query = query.where(Order.estado == estado)
    return session.exec(query).all()


@router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int, session: Session = Depends(get_session)):
    return get_order_or_404(session, order_id)


@router.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, body: Order, session: Session = Depends(get_session)):
    order = get_order_or_404(session, order_id)
    order.mesa_id = body.mesa_id
    order.mesero_id = body.mesero_id
    order.tipo_pedido = body.tipo_pedido
    order.estado = body.estado
    touch(order)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, session: Session = Depends(get_session)):
    order = get_order_or_404(session, order_id)
    for d in session.exec(select(OrderDetail).where(OrderDetail.order_id == order_id)).all():
        session.delete(d)
    session.delete(order)
    session.commit()


# ---------- CRUD de ítems del pedido ----------
@router.post("/orders/{order_id}/items", response_model=OrderDetail, status_code=status.HTTP_201_CREATED)
def add_order_item(order_id: int, detail: OrderDetail, session: Session = Depends(get_session)):
    order = get_order_or_404(session, order_id)
    product = session.get(Product, detail.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    detail.id = None
    detail.order_id = order_id
    detail.precio_unitario = product.precio  # el precio lo fija el servidor
    touch(order)
    session.add(detail)
    session.add(order)
    session.commit()
    session.refresh(detail)
    return detail


@router.get("/orders/{order_id}/items", response_model=list[OrderDetail])
def list_order_items(order_id: int, session: Session = Depends(get_session)):
    get_order_or_404(session, order_id)
    return session.exec(select(OrderDetail).where(OrderDetail.order_id == order_id)).all()


@router.put("/orders/{order_id}/items/{item_id}", response_model=OrderDetail)
def update_order_item(order_id: int, item_id: int, cantidad: int, session: Session = Depends(get_session)):
    order = get_order_or_404(session, order_id)
    item = session.get(OrderDetail, item_id)
    if not item or item.order_id != order_id:
        raise HTTPException(status_code=404, detail="Ítem no encontrado en este pedido")
    if cantidad < 1:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a 0")
    item.cantidad = cantidad
    touch(order)
    session.add(item)
    session.add(order)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/orders/{order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item(order_id: int, item_id: int, session: Session = Depends(get_session)):
    order = get_order_or_404(session, order_id)
    item = session.get(OrderDetail, item_id)
    if not item or item.order_id != order_id:
        raise HTTPException(status_code=404, detail="Ítem no encontrado en este pedido")
    session.delete(item)
    touch(order)
    session.add(order)
    session.commit()
