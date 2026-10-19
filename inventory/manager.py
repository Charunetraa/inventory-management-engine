from inventory.models import Product
from inventory.exceptions import (
    InvalidProductError,
    DuplicateProductError,
    ProductNotFoundError,
)


class InventoryManager:
    def __init__(self):
        self._products = {}

    def add_product(self, product):
        if not isinstance(product, Product):
            raise InvalidProductError("A valid Product object is required.")

        if product.product_id in self._products:
            raise DuplicateProductError(
                f"Product ID '{product.product_id}' already exists."
            )

        self._products[product.product_id] = product

    def get_product(self, product_id):
        if product_id not in self._products:
            raise ProductNotFoundError(
                f"Product '{product_id}' was not found."
            )
        return self._products[product_id]

    def get_all_products(self):
        return list(self._products.values())

    def update_product(self, product_id, name=None, price=None):
        product = self.get_product(product_id)

        if name is not None:
            if not isinstance(name, str) or not name.strip():
                raise InvalidProductError("Product name cannot be empty.")
            product._name = name.strip()

        if price is not None:
            if isinstance(price, bool) or not isinstance(price, (int, float)):
                raise InvalidProductError("Price must be numeric.")
            if price < 0:
                raise InvalidProductError("Price cannot be negative.")
            product._price = float(price)

    def remove_product(self, product_id):
        self.get_product(product_id)
        del self._products[product_id]

    def load_products(self, products):
        for product in products:
            self.add_product(product)