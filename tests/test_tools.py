"""Test utilities/tools"""
from src.tools.http import GITLAB_CLIENT


def test_gitlab_client() -> None:
    """
    Basic test to ensure correct json header is set in the client.

    Returns:
        None
    """
    assert GITLAB_CLIENT.headers['Content-Type'] == 'application/json', \
        "Should set the content-type header to 'application/json'"
