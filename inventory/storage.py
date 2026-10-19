import csv
import json
from pathlib import Path

from inventory.models import PhysicalProduct, DigitalProduct
from inventory.exceptions import InvalidProductError


class InventoryStorage:
    FIELDS = [
        "product_id",
        "name",
        "price",
        "quantity",
        "product_type",
    ]

    @staticmethod
    def _make_product(record):
        product_type = record.get("product_type", "physical")

        classes = {
            "physical": PhysicalProduct,
            "digital": DigitalProduct,
        }

        if product_type not in classes:
            raise InvalidProductError(
                f"Unknown product type: {product_type}"
            )

        return classes[product_type](
            product_id=record["product_id"],
            name=record["name"],
            price=float(record["price"]),
            quantity=int(record["quantity"]),
        )

    @classmethod
    def save_json(cls, products, filename):
        path = Path(filename)
        records = [product.to_dict() for product in products]

        with path.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)

    @classmethod
    def load_json(cls, filename):
        path = Path(filename)

        with path.open("r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise InvalidProductError(
                "JSON inventory must contain a list of products."
            )

        return [cls._make_product(record) for record in records]

    @classmethod
    def save_csv(cls, products, filename):
        path = Path(filename)

        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=cls.FIELDS)
            writer.writeheader()

            for product in products:
                writer.writerow(product.to_dict())

    @classmethod
    def load_csv(cls, filename):
        path = Path(filename)

        with path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != cls.FIELDS:
                raise InvalidProductError(
                    "CSV file has an invalid header."
                )

            return [cls._make_product(row) for row in reader]