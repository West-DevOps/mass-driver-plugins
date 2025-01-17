"""Module to deal with forging the gitlab"""
import logging

from src.tools.http import GITLAB_CLIENT
from mass_driver.models.forge import Forge
from mass_driver.models.repository import BranchName


class GitLab(Forge):
    def create_pr(self,forge_repo_url: str, base_branch: BranchName, head_branch: BranchName, pr_title: str,
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
        logging.debug(f"Creating MR fro {forge_repo_url} merging {head_branch} into {base_branch}")



    def pr_statuses(self) -> list[str]:
        """

        Returns:

        """
        return []
