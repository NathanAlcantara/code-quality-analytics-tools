from app.models import GitlabGroup, GitlabProject, HierarchyGroup, db


class GitlabRepository:
    def __init__(self, db=db) -> None:
        self.db = db

    def insert_group(self, gitlab_group):
        gitlab_group_db = GitlabGroup()
        gitlab_group_db.id = gitlab_group.id
        gitlab_group_db.name = gitlab_group.name

        self.db.session.add(gitlab_group_db)
        self.db.session.commit()

    def insert_project(self, gitlab_project, hierarchy_group_id):
        gitlab_project_db = GitlabProject()
        gitlab_project_db.name = gitlab_project.name
        gitlab_project_db.web_url = gitlab_project.web_url

        gitlab_project_db.gitlab_group_id = gitlab_project.namespace['id']
        gitlab_project_db.hierarchy_group_id = hierarchy_group_id

        self.db.session.add(gitlab_project_db)
        self.db.session.commit()

    def get_group(self, id):
        return GitlabGroup.query.filter_by(id=id).first()

    #TODO: aaa
    def get_hierarchy_group(self, id):
        return HierarchyGroup.query.filter_by(id=id).first()
