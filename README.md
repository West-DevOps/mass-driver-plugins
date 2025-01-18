# mass-driver-plugins

Plugins for [mass-driver](https://github.com/OverkillGuy/mass-driver) a bulk repo editing program. 

At the time of writing, this repo uses a forked version [mass-driver](https://github.com/w3s7y/mass-driver) which
supports `https` cloning of repos (as well as a few other improvements which are not yet back on the main repo).

## Installing and running

```shell
poetry install --with docs --with test
# Go make a PAT token on gitlab.com with API read access. 
export GITLAB_TOKEN=<your token>
poetry run mass-driver run activities/gitlab_example.toml
```

## Documentation 

The official `mass-driver` has its own [docs](https://jiby.tech/mass-driver/).

We have the [documentation here](https://west-devops.github.io/mass-driver-plugins/) for these plugins. 

### Hosting locally

Want to check the docs after an update but can't be bothered to get a merge onto `main`?... 

```shell
mkdocs serve -w src # Watch the src folder for updates (automatically watches docs and mkdocs.yml files).
# Docs are now available from http://127.0.0.1:8000/
```
