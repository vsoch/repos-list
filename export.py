#!/usr/bin/env python3

import csv
import os
import requests
import sys
import time

BASE = "https://api.github.com"
here = os.path.dirname(os.path.abspath(__file__))


def abort_if_fail(response):
    """Exit with an error and print the reason.

    Parameters:
    response (requests.Response) : an unparsed response from requests
    reason                 (str) : a message to print to the user for fail.
    """
    message = "%s: %s: %s" % (
        response.status_code,
        response.reason,
        response.json(),
    )
    sys.exit(message)


def get_headers():
    """Return headers, including a GitHub token if it's defined"""
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = "token %s" % token
    return headers


def get_user_repos(user):
    """Search the GitHub api based on finding repos greater than a minimum size."""
    url = "%s/users/%s/repos" % (BASE, user)
    repos = get_paginated_responses(url)
    print("Found %s results for user %s" % (len(repos), user))
    return repos


def get_paginated_responses(url):
    """Given a url, return paginated results"""
    headers = get_headers()
    page = 1

    data = {"per_page": 100, "page": page}
    response = requests.get(url, headers=headers, params=data)
    repos = []
    while response.json():

        # Ensure the response is still working
        if response.status_code != 200:
            abort_if_fail(response)

        data["page"] += 1
        repos += response.json()
        response = requests.get(url, headers=headers, params=data)

    return repos


def repos_to_columns(repos):
    """Given a list of GitHub repositories, convert them to columns (list of lists)
    to prepare for tsv export
    """
    data = [["NAME", "URL", "HOMEPAGE", "DESCRIPTION", "CREATED_AT"]]
    for repo in repos:
        data.append(
            [
                repo["full_name"],
                repo["html_url"],
                repo["homepage"],
                repo["description"] or "",
                repo["created_at"],
            ]
        )
    return data


def get_orgs(user):
    url = "%s/users/%s/orgs" % (BASE, user)
    orgs = get_paginated_responses(url)
    return orgs


def get_org_repos(org):
    url = "%s/orgs/%s/repos" % (BASE, org)
    return get_paginated_responses(url)


def main():

    # A username is required
    if len(sys.argv) == 1:
        sys.exit("A username is required.")
    user = sys.argv[1]

    print("Getting repos for %s" % user)
    repos = get_user_repos(user)
    orgs = get_orgs(user)

    for org in orgs:
        print("Getting repos for %s" % org["login"])
        repos = repos + get_org_repos(org["login"])
        time.sleep(5)

    # Write to csv file. Likely manual parsing would be needed
    filename = os.path.join(here, "%s-repositories.tsv" % user)
    data = repos_to_columns(repos)

    with open(filename, "w", newline="") as outfile:
        writer = csv.writer(outfile, delimiter="\t")
        [writer.writerow(row) for row in data]


if __name__ == "__main__":
    main()
