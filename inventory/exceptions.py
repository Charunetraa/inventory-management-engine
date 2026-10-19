class InventoryError(Exception):
    """Base exception for inventory-related errors."""
    pass


class InvalidProductError(InventoryError):
    """Raised when product information is invalid."""
    pass


class DuplicateProductError(InventoryError):
    """Raised when a product ID already exists."""
    pass


class ProductNotFoundError(InventoryError):
    """Raised when a product cannot be found."""
    pass


class InsufficientStockError(InventoryError):
    """Raised when requested stock is unavailable."""
    pass