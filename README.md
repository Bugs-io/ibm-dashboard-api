# ibm-dashboard-api
This project contains the back-end for the project course.

## Set up and activate virtual environment
```
python -m venv ./.venv/
source ./.venv/bin/activate
```

## Build and run docker container
```
docker build -t dashboard-app .
docker run -d -p 8000:8000 dashboard-app
```

## Contribute
In order to contribute to the project:
1. First setup git pre-commit hook for analysing python code with pylint on every commit.
```
chmod +x ./precommit-hook-setup
./precommit-hook-setup
```
2. Every commit to the codebase must pass pylint test successfully. Code must be rated 8 or greater.
