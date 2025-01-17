"""Provides httpx clients with some sane defaults"""
import os
import httpx

GITLAB_CLIENT: httpx.Client = httpx.Client(transport=httpx.HTTPTransport(retries=5), timeout=999999, headers={
    "Content-Type": "application/json",
    "PRIVATE-TOKEN": os.environ.get('GITLAB_TOKEN')
})
"""HTTP Client for the gitlab source/forge classes"""
