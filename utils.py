#! /usr/bin/env python2
import requests
from models import GithubInfo, Security, db
from datetime import datetime, timezone

def get_user_repo(user):
    sec = Security.query.order_by(Security.date_added).one()
    header = {"Authorization": f"token {sec.token}"}
    r = requests.get(f'https://api.github.com/users/{user}/repos', headers=header)
    repos = r.json()
    for repo in repos:
        if repo['fork']:
            # skip it
            continue
        url = repo['commits_url'][:-6]
        commit_info = requests.get(url)  # commit url page for a project
        commit_info = commit_info.json()  # JSON object of Commit Page for a project
        commit_times = len(commit_info)
        for commit_item in commit_info:
            for i, e in enumerate(commit_info):
                if i == 1:
                    first_commit = clean_time(e['commit']['author']['date'])  # Gets cleaned datetime for first_commit
                elif (i == (commit_times-1)):
                    last_commit = clean_time(e['commit']['author']['date'])  # Gets cleaned datetime for last_commit

        new_proj = GithubInfo(name = repo['name'], user_name = repo['owner']['login'], first_commit = first_commit,
                            last_commit = last_commit, url = repo['html_url'],
                            num_commits = commit_times, date_pulled = datetime.now(timezone.utc))
        db.session.add(new_proj)
        db.session.commit()


def clean_time(time_str):
    if 'T' in time_str:
        split_str = time_str.split('T')
        time_str = split_str[0]
    return datetime.strptime(time_str, '%Y-%m-%d')


if __name__ == '__main__':
    get_user_repo('adampizzo')
