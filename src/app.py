import flask
import logging
from user_input import UserInput
from retriever import CommitRetriever

TIMEOUT_S = 5 * 60
app = flask.Flask(__name__)

@app.route('/commit_viewer', methods=['POST'])
def commit_viewer():
    # Get url and branch from request
    r = flask.request.get_json()
    url = str(r['url'])
    if 'branch' in r:
        branch = str(r['branch'])
    else:
        branch = 'master'

    # Validate url
    uinput = UserInput()
    if not uinput.validate_url(url):
        return flask.jsonify( {'failure': 'Invalid url'})

    # Retrieve list of commits
    cr = CommitRetriever(url, branch)
    commit_list, error = cr.get_commits()
    if not error:
        return flask.jsonify( {'commit_list': commit_list})
    else:
        return flask.jsonify( {'failure': error})

if __name__ == '__main__':
    # Run flask
    app.run()