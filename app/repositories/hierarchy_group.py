from app.models import GitlabGroup, HierarchyGroup, db


class HierarchyGroupRepository:
    def __init__(self, db=db) -> None:
        self.db = db

    def insert(self, hierarchy_group):
        hierarchy_group_db = HierarchyGroup()
        hierarchy_group_db.product = hierarchy_group.product
        hierarchy_group_db.module = hierarchy_group.module
        hierarchy_group_db.manager = hierarchy_group.manager

        self.db.session.add(hierarchy_group_db)
        self.db.session.commit()

        return hierarchy_group_db
