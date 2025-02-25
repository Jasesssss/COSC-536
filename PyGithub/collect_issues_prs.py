from github import Github
import pandas as pd

g = Github("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") 

repo_names = [
    "django/django", "flask/flask", "pallets/werkzeug", "encode/starlette", "fastapi/fastapi",
    "pandas-dev/pandas", "numpy/numpy", "scikit-learn/scikit-learn", "matplotlib/matplotlib",
    "pytorch/pytorch", "tensorflow/tensorflow", "huggingface/transformers", "dask/dask",
    "statsmodels/statsmodels", "seaborn/seaborn", "psf/requests", "kennethreitz/certifi",
    "pyinstaller/pyinstaller", "ansible/ansible", "fabric/fabric", "pytest-dev/pytest",
    "tox-dev/tox", "python/mypy", "pypa/pip", "pypa/setuptools", "psf/black", "flake8/flake8",
    "scipy/scipy", "sympy/sympy", "biopython/biopython", "paramiko/paramiko", "scrapy/scrapy",
    "urllib3/urllib3", "python-telegram-bot/python-telegram-bot", "pypa/virtualenv",
    "click-contrib/click", "theacodes/coveragepy", "cookiecutter/cookiecutter", "psycopg/psycopg2",
    "sqlalchemy/sqlalchemy", "celery/celery", "boto/boto3", "home-assistant/core",
    "saltstack/salt", "jupyter/notebook", "python-poetry/poetry", "rq/rq", "pyca/cryptography",
    "arrow-py/arrow", "pendulum/pendulum", "gitpython-developers/GitPython", "redis/redis-py"
]

issue_data = []
pr_data = []

for name in repo_names:
    try:
        print(f"Processing {name}...")  
        repo = g.get_repo(name)
        
        open_issues = repo.get_issues(state="open")
        for issue in open_issues[:100]:
            issue_data.append({
                "repo": name,
                "issue_id": issue.number,
                "created_at": issue.created_at,
                "closed_at": issue.closed_at,
                "labels": [label.name for label in issue.labels]
            })
        
        closed_prs = repo.get_pulls(state="closed")
        for pr in closed_prs[:100]:
            pr_data.append({
                "repo": name,
                "pr_id": pr.number,
                "created_at": pr.created_at,
                "merged_at": pr.merged_at,
                "comments": pr.comments
            })
    except Exception as e:
        print(f"Error with {name}: {e}")  
        
# Save to CSV
pd.DataFrame(issue_data).to_csv("issue_data.csv", index=False)
pd.DataFrame(pr_data).to_csv("pr_data.csv", index=False)
print("Issues saved to issue_data.csv and PRs saved to pr_data.csv")