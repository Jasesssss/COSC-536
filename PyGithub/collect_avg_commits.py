from github import Github
import pandas as pd
import time

# GitHub token (replace with yours)
g = Github("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")

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


commit_stats = []

print(f"⏳ Fetching average commits per week for {len(repo_names)} repositories...\n")

for idx, name in enumerate(repo_names, start=1):
    print(f"[{idx}/{len(repo_names)}] Processing {name}...", end=" ", flush=True)
    start_time = time.time()

    try:
        repo = g.get_repo(name)
        stats = repo.get_stats_commit_activity()

        # GitHub may return None while stats are being calculated
        if stats is None:
            raise ValueError("GitHub is still calculating stats. Try again later.")

        weekly_commits = [week.total for week in stats]  # last 52 weeks
        avg_commits = sum(weekly_commits) / len(weekly_commits)

        commit_stats.append({
            "repo": name,
            "avg_commits_per_week": round(avg_commits, 2)
        })

        print(f"Done in {round(time.time() - start_time, 2)}s")

    except Exception as e:
        print(f"Failed: {e}")
        commit_stats.append({
            "repo": name,
            "avg_commits_per_week": "error"
        })

# Save to CSV
pd.DataFrame(commit_stats).to_csv("avg_commits_per_week.csv", index=False)
print("\n Saved to avg_commits_per_week.csv")
