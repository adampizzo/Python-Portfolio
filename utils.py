#! /usr/bin/env python2
import json
import requests

var = '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'

def get_user_repo(user):
    header = {"Authorization": f"token {var}"}
    r = requests.get(f'https://api.github.com/users/{user}/repos', headers=header)
    repos = r.json()
    repos_list = []
    print(repos)
    
    for repo in repos:
        if repo['fork']:
            # skip it
            continue
        url = repo['commits_url'][:-6]
        c = requests.get(url)
        c = c.json()
        commit_times = len(c)
        
        repos_dict = {
            'name': repo['name'],
            'html_url': repo['html_url'],
            'num_commits': commit_times
        }
        repos_list.append(repos_dict)
    return repos_list


if __name__ == '__main__':
    # r = requests.get(f'https://api.github.com/users/adampizzo/repos')
    # r = r.json()
    
    # for item in r:
    #     if item['html_url'] == "https://github.com/adampizzo/Adam-Python-Project-2":
    #         url = item['commits_url'][:-6]
    #         c = requests.get(url)
    #         c = c.json()
    #         print(len(c))
    git_adam = get_user_repo('adampizzo')
    ttl_commits = 0
    for adam in git_adam:
        ttl_commits += int(adam['num_commits'])
    print(ttl_commits)