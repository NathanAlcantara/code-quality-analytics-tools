from graphene import Boolean, List, Mutation, String

from ...services import GitlabService


class GitlabGroupsImporterMutation(Mutation):
    class Arguments:
        names = List(String, required=False)

    ok = Boolean()

    def mutate(root, info, names=None):
        gitlab_service = GitlabService()
        gitlab_service.import_groups_by_name_in_bulk(names)

        return GitlabGroupsImporterMutation(ok=True)



# class GitlabProjectsImporterMutation(Mutation):
#     class Arguments:
#         namespace = String(required=False)
#         names = List(String, required=False)

#     ok = Boolean()

#     def mutate(root, info, namespace=None, names=None):
#         gitlab_client = GitlabClient()

#         if names and not namespace:
#             return GitlabProjectsImporterMutation(ok=False)
#         elif names:
#             gitlab_projects = gitlab_client.get_projects_of_group_by_names(
#                 namespace, names)
#         elif namespace:
#             gitlab_projects = gitlab_client.get_projects_of_group(namespace)
#         else:
#             gitlab_projects = gitlab_client.get_projects()

#         print(gitlab_projects)

#         return GitlabProjectsImporterMutation(ok=True)
