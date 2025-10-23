"""
Funciones de acceso a datos para `Pedido` y `DetallePedido`. Incluye
lógica para crear un pedido con sus detalles y ajustar el stock de los
productos involucrados.
"""

from typing import List, Optional, Sequence

from peewee import DoesNotExist

from app.models.pedido import Pedido
from app.models.detalle_pedido import DetallePedido
from app.models.cliente import Cliente
from app.models.producto import Producto
from app.repositories.producto_repo import ajustar_stock, get_producto


def create_pedido(
    cliente_id: int,
    metodo_pago: str,
    items: Sequence[dict],
    direccion_entrega: str | None = None,
    instrucciones_entrega: str | None = None,
) -> Optional[Pedido]:
    """Crea un pedido con sus detalles y actualiza el inventario de
    productos. `items` debe ser una lista de diccionarios con
    `producto_id`, `cantidad` y opcionalmente `notas_personalizacion`.

    Devuelve la instancia de `Pedido` creada o `None` si falla (por
    ejemplo si no hay suficiente stock).
    """
    try:
        cliente = Cliente.get_by_id(cliente_id)
    except DoesNotExist:
        return None
    # Calcular monto total y verificar inventario
    monto_total = 0
    detalles = []
    for item in items:
        producto = get_producto(item["producto_id"])
        if not producto:
            return None
        cantidad = item.get("cantidad", 1)
        # Verificar stock disponible
        if producto.stock < cantidad:
            return None
        subtotal = float(producto.precio) * cantidad
        monto_total += subtotal
        detalles.append(
            {
                "producto": producto,
                "cantidad": cantidad,
                "precio_unitario": producto.precio,
                "colaborador": producto.colaborador,
                "notas_personalizacion": item.get("notas_personalizacion"),
            }
        )
    # Crear pedido
    pedido = Pedido.create(
        cliente=cliente,
        metodo_pago=metodo_pago,
        estatus="POR PAGAR",
        monto_total=monto_total,
        direccion_entrega=direccion_entrega,
        instrucciones_entrega=instrucciones_entrega,
    )
    # Crear detalles y ajustar inventario
    for d in detalles:
        DetallePedido.create(
            pedido=pedido,
            producto=d["producto"],
            cantidad=d["cantidad"],
            precio_unitario=d["precio_unitario"],
            colaborador=d["colaborador"],
            notas_personalizacion=d.get("notas_personalizacion"),
        )
        # Restar del stock
        # Utilizamos el identificador del producto para ajustar el stock
        ajustar_stock(d["producto"].producto_id, -d["cantidad"])
    return pedido


def get_pedido(pedido_id: int) -> Optional[Pedido]:
    try:
        return Pedido.get(Pedido.pedido_id == pedido_id)
    except Pedido.DoesNotExist:
        return None


def list_pedidos(skip: int = 0, limit: int = 50) -> List[Pedido]:
    return list(Pedido.select().offset(skip).limit(limit))


def update_pedido_status(pedido_id: int, estatus: str) -> Optional[Pedido]:
    """Actualiza el estatus de un pedido (por ejemplo, a PAGADO, ENTREGADO o
    CANCELADO). Si se marca como CANCELADO se devuelve el stock al
    inventario.
    """
    pedido = get_pedido(pedido_id)
    if not pedido:
        return None
    # Si se cancela el pedido, reponer stock
    if estatus.upper() == "CANCELADO" and pedido.estatus != "CANCELADO":
        # devolver stock de cada detalle
        for detalle in pedido.detalles:
            ajustar_stock(detalle.producto.producto_id, detalle.cantidad)
    pedido.estatus = estatus.upper()
    pedido.save()
    return pedido