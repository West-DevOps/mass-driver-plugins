"""Module to deal with forging the gitlab.

This forge reads the environment variable `GITLAB_TOKEN` in order to authenticate with the gitlab API and raise MRs.
"""
import json
import logging
from urllib.parse import quote

from src.tools.http import GITLAB_CLIENT
from mass_driver.models.forge import Forge
from mass_driver.models.repository import BranchName


class GitLab(Forge):
    def create_pr(self, forge_repo_url: str, base_branch: BranchName, head_branch: BranchName, pr_title: str,
                  pr_body: str, draft: bool) -> str:
        """
        Create a merge request in gitlab via the API
        Args:
            forge_repo_url:
            base_branch:
            head_branch:
            pr_title:
            pr_body:
            draft:

        Returns:
            Link to the MR
        """
        logging.info(forge_repo_url)
        logging.debug(f"Creating MR fro {forge_repo_url} merging {head_branch} into {base_branch}")

        response = GITLAB_CLIENT.post(url=forge_repo_url, json={
            "source_branch": head_branch,
            "target_branch": base_branch,
            "title": pr_title,
            "description": pr_body
        })
        return json.loads(response.text)['web_url']

    def pr_statuses(self) -> list[str]:
        """

        Returns:

        """
        return []
