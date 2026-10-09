class OrderError(Exception):
    """Excepción base del dominio."""


class InvalidOrderError(OrderError):
    """Indica que una orden incumple las reglas del dominio."""


class OrderNotFoundError(OrderError):
    """Indica que la orden solicitada no existe."""


class NotificationError(OrderError):
    """Indica que no se pudo enviar una notificación."""
