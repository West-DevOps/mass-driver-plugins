"""Module to test our forge plugins"""
import httpx

import src.tools.http
from src.forges.gitlab import GitLab


def test_gitlab_forge(mocker) -> None:
    """
    Tests the gitlab forge (pr creator)

    Args:
        mocker: the mocker fixture

    Returns:
        None - just runs assertions
    """
    mocked_data = '{"web_url": "https://gitlab.com/some/pr"}'
    mock_response = httpx.Response(status_code=201, text=mocked_data, headers={})
    mock = mocker.patch('src.forges.gitlab.GITLAB_CLIENT.post', return_value=mock_response)

    forge = GitLab()
    forge.create_pr(
        forge_repo_url="https://gitlab.com/api/v4/projects/66255506/merge_requests",
        base_branch="main",
        head_branch="feat/test",
        pr_title="Test",
        pr_body="Some test PR",
        draft=False
    )

    mock.assert_called_once_with(url="https://gitlab.com/api/v4/projects/66255506/merge_requests", json={
        "source_branch": 'feat/test',
        "target_branch": 'main',
        "title": 'Test',
        "description": 'Some test PR'
    }), "Should have been called with proper args"

