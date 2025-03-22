from github import Github
import pandas as pd
import time

# GitHub token (replace with yours)
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

team_sizes = []

print(f"⏳ Fetching contributor count for {len(repo_names)} repositories...\n")

for idx, name in enumerate(repo_names, start=1):
    print(f"[{idx}/{len(repo_names)}] Processing {name}...", end=" ", flush=True)
    start_time = time.time()

    try:
        repo = g.get_repo(name)
        contributors = repo.get_contributors()
        count = 0
        for _ in contributors:
            count += 1
        team_sizes.append({
            "repo": name,
            "team_size": count
        })
        print(f"✅ Done in {round(time.time() - start_time, 2)}s")

    except Exception as e:
        print(f"⚠️ Failed: {e}")
        team_sizes.append({
            "repo": name,
            "team_size": "error"
        })

# Save to CSV
pd.DataFrame(team_sizes).to_csv("team_size.csv", index=False)
print("\n✅ Saved to team_size.csv")
