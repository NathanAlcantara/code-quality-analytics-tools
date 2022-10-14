from graphene import ObjectType

from .creater import GitlabProjectCreateMutation
from .example import ExampleMutation
from .importer import GitlabGroupsImporterMutation
from .inserter import HierarchyGroupInserterMutation


class Mutations(ObjectType):
    example = ExampleMutation.Field()
    import_gitlab_group = GitlabGroupsImporterMutation.Field()
    insert_hierarchy_group = HierarchyGroupInserterMutation.Field()
    create_gitlab_project = GitlabProjectCreateMutation.Field()
