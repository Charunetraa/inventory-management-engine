import pytest

from inventory.models import PhysicalProduct, DigitalProduct
from inventory.manager import InventoryManager
from inventory.storage import InventoryStorage
from inventory.exceptions import (
    InvalidProductError,
    DuplicateProductError,
    ProductNotFoundError,
    InsufficientStockError,
)


@pytest.fixture
def manager():
    inventory = InventoryManager()
    inventory.add_product(
        PhysicalProduct("P101", "Notebook", 50.0, 20)
    )
    return inventory


def test_product_creation_and_type():
    physical = PhysicalProduct("P1", "Book", 25, 5)
    digital = DigitalProduct("D1", "E-book", 100, 10)

    assert physical.product_type() == "physical"
    assert digital.product_type() == "digital"
    assert physical.to_dict()["quantity"] == 5


@pytest.mark.parametrize(
    "args",
    [
        ("", "Book", 10, 2),
        ("P1", "", 10, 2),
        ("P1", "Book", -1, 2),
        ("P1", "Book", "bad", 2),
        ("P1", "Book", 10, -2),
        ("P1", "Book", 10, 1.5),
    ],
)
def test_invalid_product(args):
    with pytest.raises(InvalidProductError):
        PhysicalProduct(*args)


def test_stock_operations():
    product = PhysicalProduct("P1", "Book", 20, 5)
    product.add_stock(3)
    assert product.quantity == 8

    product.remove_stock(2)
    assert product.quantity == 6

    with pytest.raises(InsufficientStockError):
        product.remove_stock(10)

    with pytest.raises(InvalidProductError):
        product.add_stock(0)


def test_add_search_list_and_remove(manager):
    assert manager.get_product("P101").name == "Notebook"
    assert len(manager.get_all_products()) == 1

    with pytest.raises(DuplicateProductError):
        manager.add_product(
            PhysicalProduct("P101", "Another book", 30, 1)
        )

    manager.add_product(
        DigitalProduct("D101", "E-book", 100, 10)
    )
    assert len(manager.get_all_products()) == 2

    manager.remove_product("P101")
    assert len(manager.get_all_products()) == 1

    with pytest.raises(ProductNotFoundError):
        manager.get_product("MISSING")


def test_update_product(manager):
    manager.update_product("P101", name="New Notebook", price=60)
    product = manager.get_product("P101")

    assert product.name == "New Notebook"
    assert product.price == 60.0

    with pytest.raises(InvalidProductError):
        manager.update_product("P101", name="")

    with pytest.raises(InvalidProductError):
        manager.update_product("P101", price=-1)


def test_reject_non_product(manager):
    with pytest.raises(InvalidProductError):
        manager.add_product("not a product")


def test_json_persistence(manager, tmp_path):
    path = tmp_path / "inventory.json"

    InventoryStorage.save_json(manager.get_all_products(), path)
    loaded = InventoryStorage.load_json(path)

    assert len(loaded) == 1
    assert loaded[0].name == "Notebook"
    assert loaded[0].product_type() == "physical"


def test_csv_persistence(manager, tmp_path):
    path = tmp_path / "inventory.csv"

    InventoryStorage.save_csv(manager.get_all_products(), path)
    loaded = InventoryStorage.load_csv(path)

    assert len(loaded) == 1
    assert loaded[0].product_id == "P101"


def test_invalid_csv_header(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("wrong,header\n1,2\n", encoding="utf-8")

    with pytest.raises(InvalidProductError):
        InventoryStorage.load_csv(path)


def test_unknown_product_type(tmp_path):
    path = tmp_path / "unknown.json"
    path.write_text(
        '[{"product_id":"X1","name":"Item","price":5,'
        '"quantity":1,"product_type":"unknown"}]',
        encoding="utf-8",
    )

    with pytest.raises(InvalidProductError):
        InventoryStorage.load_json(path)


def test_invalid_json_structure(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"product_id": "P1"}', encoding="utf-8")

    with pytest.raises(InvalidProductError):
        InventoryStorage.load_json(path)