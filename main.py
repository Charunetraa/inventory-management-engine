from inventory.models import PhysicalProduct, DigitalProduct
from inventory.manager import InventoryManager
from inventory.storage import InventoryStorage
from inventory.exceptions import InventoryError


def main():
    inventory = InventoryManager()

    try:
        inventory.add_product(
            PhysicalProduct("P101", "Notebook", 50.0, 20)
        )
        inventory.add_product(
            DigitalProduct("D101", "Python E-book", 199.0, 50)
        )

        print("INVENTORY MANAGEMENT ENGINE")
        print("-" * 30)

        for product in inventory.get_all_products():
            print(
                f"{product.product_id} | {product.name} | "
                f"₹{product.price:.2f} | "
                f"Stock: {product.quantity} | "
                f"Type: {product.product_type()}"
            )

        InventoryStorage.save_json(
            inventory.get_all_products(), "inventory.json"
        )
        InventoryStorage.save_csv(
            inventory.get_all_products(), "inventory.csv"
        )

        print("\nInventory saved to inventory.json and inventory.csv.")

    except InventoryError as error:
        print(f"Inventory error: {error}")


if __name__ == "__main__":
    main()