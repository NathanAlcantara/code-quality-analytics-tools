from graphene import Boolean, Int, Mutation, String

from ...services import GitlabService


class GitlabProjectCreateMutation(Mutation):
    class Arguments:
        namespace = String()
        name = String()
        hierarchy_group_id = Int()

    ok = Boolean()

    def mutate(root, info, namespace, name, hierarchy_group_id):
        gitlab_service = GitlabService()
        gitlab_service.insert_project(namespace, name, hierarchy_group_id)

        return GitlabProjectCreateMutation(ok=True)
