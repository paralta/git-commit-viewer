# Git commit viewer

## List commits from GitHub url

```
cd src
python3 main.py
```

## List commits using Flask app

```
cd src
pip3 install -r requirements.txt
python3 app.py
curl -X POST http://localhost:5000/commit_viewer -H 'Content-Type: application/json' -d '{"url": "<url>", "branch": "<branch>", "num_commits": <num_commits>}'
```

## List commits using Docker

```
docker build -t commit-viewer .
docker run -dp 5000:5000 commit-viewer
```

## Run unit tests

```
cd src
./run_unittests.sh
```