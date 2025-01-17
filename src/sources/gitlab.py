"""Module for interacting with gitlab"""
import json
import re
from enum import Enum

from src.tools.http import GITLAB_CLIENT
from mass_driver.models.repository import Source, IndexedRepos


REQ_OPTS = "pagination=keyset&order_by=id&simple=true&per_page=100"
"""Default request options"""


class CloneMode(Enum):
    HTTP = 'http'
    SSH = 'ssh'


class GitLabSearch(Source):
    """Class for performing basic search for repos.  Also, gitlabs search function SUCKS so YMMV..."""

    api_root: str
    """API Root for your Gitlab instance"""

    search_query: str
    """Query to search with"""

    clone_mode: CloneMode
    """Return HTTP or SSH clone links?"""


    def get_repos(self, repos: list, pag=None) -> None:
        """
        Gets all repos that the GITLAB_TOKEN has access to from the gitlab API that match the  `self.search_query` field.

        This can take a long time to run if you have tens of thousands of repos that match the filter!

        Returns:
            None - appends to `repos` parameter
        """
        response = GITLAB_CLIENT.get(pag or f"{self.api_root}/projects?{REQ_OPTS}&search={self.search_query}")

        for repo in json.loads(response.text):
            repos.append(repo)

        try:
            self.get_repos(repos, response.headers['link'].strip('<').split('>')[0])
        except KeyError as ke:
            print(f"No {ke} in response headers, Gitlab repo pull complete")


    def discover(self) -> IndexedRepos:
        """
        The main function called by mass driver to get list of repos to clone.

        Returns:
            Repositories that match `self.search_query`
        """
        repos = IndexedRepos()

        gitlab_repos = []
        self.get_repos(gitlab_repos)

        regex = re.compile(self.base)

        for repo in gitlab_repos:
            print(repo)

        return repos