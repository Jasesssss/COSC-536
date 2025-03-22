from github import Github
import pandas as pd
import time

# GitHub authentication
g = Github("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")

# List of repositories
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

MAX_ISSUES = 1000
issue_counts = []

print(f"⏳ Starting issue count for {len(repo_names)} repositories...\n")

for idx, name in enumerate(repo_names, start=1):
    print(f"[{idx}/{len(repo_names)}] Processing {name}...", end=" ", flush=True)
    start_time = time.time()

    try:
        repo = g.get_repo(name)
        issues = repo.get_issues(state="all", sort="created", direction="desc")

        open_count = 0
        closed_count = 0
        fetched = 0

        for issue in issues:
            if issue.pull_request is not None:
                continue  

            if issue.state == "open":
                open_count += 1
            elif issue.state == "closed":
                closed_count += 1

            fetched += 1
            if fetched >= MAX_ISSUES:
                break

        issue_counts.append({
            "repo": name,
            "open_issues_latest": open_count,
            "closed_issues_latest": closed_count,
            "total_issues_latest": open_count + closed_count
        })

        elapsed = round(time.time() - start_time, 2)
        print(f"Done in {elapsed}s")

    except Exception as e:
        elapsed = round(time.time() - start_time, 2)
        print(f"Failed in {elapsed}s: {e}")
        issue_counts.append({
            "repo": name,
            "open_issues_latest": "error",
            "closed_issues_latest": "error",
            "total_issues_latest": "error"
        })

# Save the results
df = pd.DataFrame(issue_counts)
df.to_csv("issue_counts_summary.csv", index=False)

print("\n Finished all repositories.")
print("📄 Results saved to issue_counts_summary.csv")