from items.repo.item_repo import Repo
from items.services.inventory_service import InventoryService

def test_delete_existing_item_removes_it():
    repo = Repo()
    service = InventoryService(repo)

    created = repo.create(name="apples", qty=1)
    assert repo.get(created.id) is not None

    service.delete_item(created.id)
    assert repo.get(created.id) is None

def test_delete_missing_item_is_idempotent():
    repo = Repo()
    service = InventoryService(repo)
    service.delete_item(9999)
