from abc import ABC, abstractmethod

from inventory.exceptions import InvalidProductError


class Product(ABC):
    def __init__(self, product_id, name, price, quantity):
        if not isinstance(product_id, str) or not product_id.strip():
            raise InvalidProductError("Product ID cannot be empty.")

        if not isinstance(name, str) or not name.strip():
            raise InvalidProductError("Product name cannot be empty.")

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise InvalidProductError("Price must be numeric.")

        if price < 0:
            raise InvalidProductError("Price cannot be negative.")

        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise InvalidProductError("Quantity must be an integer.")

        if quantity < 0:
            raise InvalidProductError("Quantity cannot be negative.")

        self._product_id = product_id.strip()
        self._name = name.strip()
        self._price = float(price)
        self._quantity = quantity

    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def quantity(self):
        return self._quantity

    def add_stock(self, amount):
        if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
            raise InvalidProductError("Stock addition must be a positive integer.")
        self._quantity += amount

    def remove_stock(self, amount):
        if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
            raise InvalidProductError("Stock removal must be a positive integer.")

        if amount > self._quantity:
            from inventory.exceptions import InsufficientStockError
            raise InsufficientStockError("Not enough stock available.")

        self._quantity -= amount

    @abstractmethod
    def product_type(self):
        pass

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "product_type": self.product_type(),
        }


class PhysicalProduct(Product):
    def product_type(self):
        return "physical"


class DigitalProduct(Product):
    def product_type(self):
        return "digital"