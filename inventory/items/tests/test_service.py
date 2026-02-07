from items.domain.errors import InvariantError
from items.repo.item_repo import Repo
from items.services.inventory_service import InventoryService
from items.shared.result import Ok, Err



def test_create_valid_item_persists():
    repo = Repo()
    service = InventoryService(repo)

    result = service.create_item("Milk", 2)

    assert isinstance(result, Ok)
    item = result.value

    persisted = repo.get(item.id)
    assert persisted is not None

    assert item.name == "milk"     

    assert item.qty == 2


def test_create_rejects_empty_name_and_does_not_persist():
    repo = Repo()
    service = InventoryService(repo)

    result = service.create_item("   ", 1)

    assert isinstance(result, Err)
    assert isinstance(result.error, InvariantError)
    assert repo.list() == {}


def test_create_rejects_negative_qty_and_does_not_persist():
    repo = Repo()
    service = InventoryService(repo)

    result = service.create_item("apple", -1)

    assert isinstance(result, Err)
    assert isinstance(result.error, InvariantError)  
    assert repo.list() == {}




def test_delete_missing_item_is_idempotent():
    repo = Repo()
    service = InventoryService(repo)

    result = service.delete_item("does-not-exist")

    assert result is None

    assert repo.list() == {}
