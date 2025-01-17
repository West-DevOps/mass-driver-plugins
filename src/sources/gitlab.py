"""Module for interacting with gitlab"""
import json
import logging

from src.tools.http import GITLAB_CLIENT
from mass_driver.models.repository import Source, IndexedRepos, SourcedRepo


class GitLabSearch(Source):
    """Class for performing basic search for repos.  Also, gitlabs search function SUCKS so YMMV..."""

    api_root: str
    """API Root for your Gitlab instance"""

    search_query: str
    """Query to search with"""

    clone_mode: str = "ssh"
    """Return HTTP or SSH clone links?"""

    request_opts: str = "simple=true&per_page=100"
    """Additional request options for gitlab API /projects endpoint"""


    def get_repos(self, repos: list, pag=None) -> None:
        """
        Gets all repos that the GITLAB_TOKEN has access to from the gitlab API that match the  `self.search_query` field.

        This can take a long time to run if you have tens of thousands of repos that match the filter!

        Returns:
            None - appends to `repos` parameter
        """
        response = GITLAB_CLIENT.get(pag or f"{self.api_root}/projects"
                                            f"?search={self.search_query}&pagination=keyset&order_by=id&"
                                            f"{self.request_opts}")

        for repo in json.loads(response.text):
            repos.append(repo)

        try:
            self.get_repos(repos, response.headers['link'].strip('<').split('>')[0])
        except KeyError as ke:
            logging.debug(f"No {ke} in response headers, Gitlab repo pull complete")


    def discover(self) -> IndexedRepos:
        """
        The main function called by mass driver to get list of repos to clone.

        Returns:
            Repositories that match `self.search_query`
        """
        repos = IndexedRepos()

        gitlab_repos = []
        self.get_repos(gitlab_repos)

        logging.info(f"Retrieved {len(gitlab_repos)} repos from gitlab.")

        for repo in gitlab_repos:
            repos.update({repo['name']: SourcedRepo(
                clone_url=(repo['http_url_to_repo'] if self.clone_mode == 'http' else repo['ssh_url_to_repo']),
                repo_id=repo['name'],
                force_pull=True,
                patch_data=repo
            )})

        return repos
