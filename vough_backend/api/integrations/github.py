import os
import json
import requests
from github import Github

from .file import *

class File:
    def get_organizations(self):
        file = 'api/integrations/file/orgs.json'
        if not file_exists(file):
            create_file(file)
        return read_file(file)

class GithubApi:
    API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

    def get_organization(self, login: str):
        self.login = login

        GITHUB_TOKEN = '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'
        GTHUB = Github(GITHUB_TOKEN)

        file = 'api/integrations/file/orgs.json'

        if not file_exists(file):
            create_file(file)

        organization = GTHUB.get_organization(self.login)
        name = organization.name
        public_repos = organization.public_repos
        followers = organization.get_public_members().totalCount
        score = followers + public_repos

        org = {'login': login, 'name': name, 'score': score}

        store_org(file, org)

        for org in read_file(file):
            if org['login'] == login:
                return org

    def delete(r, login: str):
        file = 'api/integrations/file/orgs.json'
        delete_org(login)
        return read_file(file)

