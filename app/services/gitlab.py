from typing import List

from ..clients import GitlabClient
from ..repositories import GitlabRepository


class GitlabService:
    def __init__(self) -> None:
        self.client = GitlabClient()
        self.repository = GitlabRepository()

    def import_groups_by_name_in_bulk(self, names: List[str]):
        if names:
            gitlab_groups = self.client.get_groups_by_names(names)
        else:
            gitlab_groups = self.client.get_groups()

        for gitlab_group in gitlab_groups:
            self.repository.insert_group(gitlab_group)

    def insert_project(self, namespace: str, name: str, hierarchy_group_id: int):
        gitlab_project = self.client.get_project(namespace, name)
        self.repository.insert_project(gitlab_project, hierarchy_group_id)
