# Git commit viewer

Given a GitHub URL for a certain repository, this service is able to provide the correspondent list of commits. It will use GitHub API to retrieve the commit information. However, if this fails, git CLI will be used.

## Run

**Option 1**

Using the terminal, run the commands below and follow the instructions provided. Python 3.7+ required.

```
cd src
python3 main.py
```

**Option 2**

To retrieve a list of commits using a Flask application, run the commands below and make a POST request. Python 3.7+ required.

```
cd src
pip3 install -r requirements.txt
python3 app.py
```

**Option 3**

To retrieve a list of commits using a Docker container, run the commands below and make a POST request

```
docker build -t commit-viewer .
docker run -dp 5000:5000 commit-viewer
```

**Make a POST request**

```
curl -X POST http://localhost:5000/commit_viewer -H 'Content-Type: application/json' -d '{"url": "<url>", "branch": "<branch>", "num_commits": <num_commits>}'
```

**Run unit tests**

```
cd src
./run_unittests.sh
```