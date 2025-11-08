"""
Rutas para validación de acceso administrativo y gestión del panel de control.
"""

from fastapi import APIRouter, HTTPException, Security
from pydantic import BaseModel
import os
from app.api.deps import get_api_key
from app.repositories.cliente_repo import get_cliente_by_usuario

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Security(get_api_key)],
)


class AdminPasswordRequest(BaseModel):
    """Esquema para validar contraseña del panel admin."""
    usuario: str
    password: str


class AdminAccessValidation(BaseModel):
    """Respuesta de validación de acceso admin."""
    access_granted: bool
    message: str
    usuario: str = None
    nombre: str = None


# Obtener contraseña de variables de entorno
ADMIN_PANEL_PASSWORD = os.getenv("ADMIN_PANEL_PASSWORD", "6605p")


@router.post("/validate-access", response_model=AdminAccessValidation)
def validate_admin_access(payload: AdminPasswordRequest):
    """
    Valida si un usuario tiene acceso al panel de control.
    
    Requiere:
    1. Que el usuario exista en la BD
    2. Que sea administrador (es_admin = True)
    3. Que proporcione la contraseña correcta del panel
    
    Args:
        payload: Contiene usuario y contraseña
        
    Returns:
        AdminAccessValidation con status de acceso
    """
    usuario = payload.usuario.strip()
    password = payload.password.strip()
    
    # Validar contraseña del panel
    if password != ADMIN_PANEL_PASSWORD:
        raise HTTPException(
            status_code=403,
            detail="Contraseña de panel incorrecta"
        )
    
    # Buscar usuario en BD
    cliente = get_cliente_by_usuario(usuario)
    
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    
    # Validar que sea administrador
    if not cliente.es_admin:
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos de administrador"
        )
    
    # Acceso concedido
    return AdminAccessValidation(
        access_granted=True,
        message="Acceso al panel concedido",
        usuario=cliente.usuario,
        nombre=cliente.nombre
    )


@router.get("/check-admin/{usuario}")
def check_admin_status(usuario: str):
    """
    Verifica si un usuario es administrador (sin validar contraseña).
    
    Útil para mostrar/ocultar botones en el frontend.
    
    Args:
        usuario: Nombre de usuario a verificar
        
    Returns:
        {"is_admin": bool, "usuario": str}
    """
    cliente = get_cliente_by_usuario(usuario.strip())
    
    if not cliente:
        return {"is_admin": False, "usuario": usuario}
    
    return {
        "is_admin": cliente.es_admin,
        "usuario": cliente.usuario,
        "nombre": cliente.nombre
    }