from items.repo.item_repo import Repo


class InventoryService:
    def __init__(self, repo:Repo) -> None:
        self.repo = repo

    def delete_item(self, item_id:int) -> None:
        self.repo.delete(item_id)