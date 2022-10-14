import json
import os
from collections import namedtuple


class EnvironmentConfiguration:
    def __init__(self):
        stream = open(self._find_config(), "r", encoding="utf-8")
        self.config = json.load(stream)
        stream.close()

    def sonarqube(self):
        sonarqube_config = namedtuple(
            "SonarQubeConfig", ["url", "token"])

        return sonarqube_config(self.config["sonarQubeUrl"], self.config["sonarQubeToken"])

    def gitlab(self):
        sonarqube_config = namedtuple(
            "GitlabConfig", ["url", "token"])

        return sonarqube_config(self.config["gitlabUrl"], self.config["gitlabToken"])

    @staticmethod
    def _find_config():
        filename = "config.json"
        result = []

        # Wlaking top-down from the root
        for root, _, files in os.walk(os.getcwd()):
            if filename in files:
                result.append(os.path.join(root, filename))

        return result[0]
