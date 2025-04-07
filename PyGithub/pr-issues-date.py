# Updated scripts for limited repo set and capturing PR/issue timestamps

from github import Github
import pandas as pd
from datetime import datetime

# Authenticate with GitHub
g = Github("")

# Use only the first 15 projects
repo_names = [
    "django/django", "pallets/werkzeug", "encode/starlette", "fastapi/fastapi",
    "pandas-dev/pandas", "numpy/numpy", "scikit-learn/scikit-learn", "matplotlib/matplotlib",
    "pytorch/pytorch", "tensorflow/tensorflow", "huggingface/transformers", "dask/dask",
    "statsmodels/statsmodels", "seaborn/seaborn", "psf/requests", "kennethreitz/certifi",
    "pyinstaller/pyinstaller", "ansible/ansible", "fabric/fabric", "pytest-dev/pytest",
    "tox-dev/tox", "python/mypy", "pypa/pip", "pypa/setuptools", "psf/black",
    "scipy/scipy", "sympy/sympy", "biopython/biopython", "paramiko/paramiko", "scrapy/scrapy",
    "urllib3/urllib3", "python-telegram-bot/python-telegram-bot", "pypa/virtualenv",
    "cookiecutter/cookiecutter", "psycopg/psycopg2", "sqlalchemy/sqlalchemy", "celery/celery",
    "boto/boto3", "home-assistant/core", "saltstack/salt", "jupyter/notebook",
    "python-poetry/poetry", "rq/rq", "pyca/cryptography", "arrow-py/arrow",
    "gitpython-developers/GitPython", "redis/redis-py"
]

# Store issue and PR data
issue_data = []
pr_data = []

# Loop through repos
for name in repo_names:
    try:
        print(f"Processing {name}...")
        repo = g.get_repo(name)

        # Fetch open and closed issues (limit 100 each for practicality)
        open_issues = repo.get_issues(state="open")
        closed_issues = repo.get_issues(state="closed")

        for issue in open_issues[:50]:
            if issue.pull_request is None:
                issue_data.append({
                    "repo": name,
                    "issue_id": issue.number,
                    "created_at": issue.created_at,
                    "closed_at": issue.closed_at,
                    "state": issue.state,
                    "labels": [label.name for label in issue.labels]
                })

        for issue in closed_issues[:50]:
            if issue.pull_request is None:
                issue_data.append({
                    "repo": name,
                    "issue_id": issue.number,
                    "created_at": issue.created_at,
                    "closed_at": issue.closed_at,
                    "state": issue.state,
                    "labels": [label.name for label in issue.labels]
                })

        # Fetch closed PRs
        closed_prs = repo.get_pulls(state="closed")
        for pr in closed_prs[:100]:
            pr_data.append({
                "repo": name,
                "pr_id": pr.number,
                "created_at": pr.created_at,
                "merged_at": pr.merged_at,
                "closed_at": pr.closed_at,
                "comments": pr.comments
            })

    except Exception as e:
        print(f"Error with {name}: {e}")

# Save to CSV
pd.DataFrame(issue_data).to_csv("limited_issue_data.csv", index=False)
pd.DataFrame(pr_data).to_csv("limited_pr_data.csv", index=False)
print("✅ Saved issue and PR data for 15 projects")
