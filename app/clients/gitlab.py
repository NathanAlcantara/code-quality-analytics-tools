from operator import truediv
from typing import List

from gitlab import Gitlab

from ..configs import EnvironmentConfiguration


class GitlabClient:
    def __init__(self):
        env_config = EnvironmentConfiguration()
        gitlab_config = env_config.gitlab()

        self.gitlab = Gitlab(url=gitlab_config.url,
                             private_token=gitlab_config.token)

    def get_groups(self):
        return self.gitlab.groups.list(iterator=True)

    def get_groups_by_names(self, names: List[str]):
        for name in names:
            yield self.gitlab.groups.get(name)

    def get_project(self, namespace: str, name: str):
        project_name_with_namespace = f"{namespace}/{name}"
        return self.gitlab.projects.get(project_name_with_namespace)

    def get_projects(self):
        return self.gitlab.projects.list(iterator=True)

    # def get_projects_of_group(self, group_id_or_name: str | int):
    #     group = self.gitlab.groups.get(group_id_or_name, lazy=True)
    #     return group.projects.list(iterator=True)

    # def get_projects_of_group_by_names(self, group_name: str, projects_names: List[str]):
    #     for name in projects_names:
    #         yield self.get_project(group_name, name)
