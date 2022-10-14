from sonarqube import SonarQubeClient as SonarQubeCommunityClient

from ..configs import EnvironmentConfiguration


class SonarQubeClient:
    def __init__(self):
        env_config = EnvironmentConfiguration()
        sonar_config = env_config.sonarqube()

        self.sonarqube = SonarQubeCommunityClient(
            sonarqube_url=sonar_config.url, token=sonar_config.token)

    def get_projects(self):
        raw_projects = self.sonarqube.projects.search_projects()

        for project in raw_projects:
            links = self.get_external_links_of_project(project['key'])

            project['links'] = links

            yield project

    def get_external_links_of_project(self, project_key):
        return self.sonarqube.project_links.search_project_links(project_key)['links']
