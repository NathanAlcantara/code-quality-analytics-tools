from collections import namedtuple

from graphene import Int, Mutation, String

from ...repositories import HierarchyGroupRepository


class HierarchyGroupInserterMutation(Mutation):
    class Arguments:
        product = String()
        module = String()
        manager = String()

    hierarchy_group_id = Int()

    def mutate(root, info, product, module, manager):
        hierarchy_group = namedtuple(
            "HierarchyGroup", ['product', 'module', 'manager'])

        hierarchy_group.product = product
        hierarchy_group.module = module
        hierarchy_group.manager = manager

        hierarchy_group_repository = HierarchyGroupRepository()
        hierarchy_group_db = hierarchy_group_repository.insert(hierarchy_group)

        return HierarchyGroupInserterMutation(hierarchy_group_id=hierarchy_group_db.id)
