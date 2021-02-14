import json
import requests

class GithubApiCommitRetriever:
    '''
    Retrieve commit list using github API
    '''
    # TODO investigate list commits API for not master branch
    commits = []

    def __init__(self, url):
        url = url.replace('https://github.com/', '').replace('.git', '')
        self.r = requests.get('https://api.github.com/repos/' + url + '/commits',
                              headers={"Accept": "application/vnd.github.v3+json"})

    def request_successful(self):
        return self.r.status_code == 200

    def commit_parser(self):
        commits_json = json.loads(self.r.text)
        for i in commits_json:
            author = i['commit']['author']
            self.commits.append({'sha': i['sha'], 'author': author['name'],
                                 'date': author['date'], 'message': i['commit']['message'].split('\n\n')})

    def get_commits(self):
        self.commit_parser()
        return self.commits