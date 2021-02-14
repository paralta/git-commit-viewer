import flask
import logging
import multiprocessing
from user_input import UserInput
from retriever import CommitRetriever

TIMEOUT_S = 5 * 60  # 5 min
app = flask.Flask(__name__)


class GitCLICommitRetriever:
    '''
    Retrieve commit list using git command-line interface
    '''
    url = ''
    branch = ''

    def __init__(self, url, branch):
        self.url = url
        self.branch = branch

    def process_commits(self, return_dict):
        cr = CommitRetriever(self.url, self.branch)
        c, err = cr.get_commits()
        return_dict[0] = {'commits': c, 'err': err}

    def get_commits(self):
        # Create a shared variable
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        # Start process_commits as a process
        p = multiprocessing.Process(
            target=self.process_commits, args=(return_dict,))
        p.start()

        # Wait for timeout seconds or until process finishes
        p.join(TIMEOUT_S)

        # If thread is still active when timeout finishes
        if p.is_alive():
            p.terminate()
            p.join()
            return [], 'Commit retriever timed out'

        return return_dict[0]['commits'], return_dict[0]['err']


@app.route('/commit_viewer', methods=['POST'])
def commit_viewer():
    # Get url, branch and number of commits from request
    r = flask.request.get_json()
    url = str(r['url'])
    branch = str(r['branch']) if 'branch' in r else 'master'
    num_commits = int(r['num_commits']) if 'num_commits' in r else 2

    # Validate url
    uinput = UserInput()
    if not uinput.validate_url(url):
        return flask.jsonify({'failure': 'Invalid url'})

    # Retrieve list of commits
    gitcli = GitCLICommitRetriever(url, branch)
    commit_list, error = gitcli.get_commits()

    # Return error message if retriever fails
    if error:
        return flask.jsonify({'failure': error})

    # Respond with restricted number of commits
    elif len(commit_list) > num_commits:
        commit_list_short = commit_list[:num_commits]
        return flask.jsonify({'commit_list': commit_list_short, 'total_num_commits': len(commit_list)})

    # Respond with unrestricted number of commits
    else:
        return flask.jsonify({'commit_list': commit_list})


if __name__ == '__main__':
    # Run flask
    app.run()
