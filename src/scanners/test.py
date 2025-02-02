import json
from pathlib import Path


def get_org_node_pkgs(repo: Path) -> dict[str, str]:
    """
    Opens a repos root level `package.json` and reads out any deps that start with `@types/`

    Args:
        repo: The repo to work on.

    Returns:
        Dictionary of { package : version } strings.
    """
    pkg_json = json.load(open(repo.joinpath('package.json'), 'r'))
    deps = pkg_json['dependencies']
    deps.update(pkg_json['devDependencies'])
    return { pkg: deps.get(pkg) for pkg in deps if pkg.startswith('@types/')}
