import flask
import logging
from user_input import UserInput
from retriever import CommitRetriever

TIMEOUT_S = 5 * 60
app = flask.Flask(__name__)


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
    cr = CommitRetriever(url, branch)
    commit_list, error = cr.get_commits()

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
