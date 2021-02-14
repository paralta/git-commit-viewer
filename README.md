# Git commit viewer

## List commits from GitHub url

```
cd src
python3 main.py
```

## List commits from GitHub url using Flask app

```
cd src
python3 app.py
curl -X POST http://localhost:5000/commit_viewer -H 'Content-Type: application/json' -d '{"url": "<url>", "branch": "<branch>"}'
```

## Run unit tests

```
cd src
./run_unittests.sh
```