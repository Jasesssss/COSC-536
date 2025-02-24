from github import Github
import pandas as pd

# Authenticate with GitHub API (replace with your token)
g = Github("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")  # Replace with your actual token

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

# Store metadata
repo_data = []
for name in repo_names:
    try:
        print(f"Fetching: {name}")  # Debug: Show which repo is being processed
        repo = g.get_repo(name)
        repo_data.append({
            "name": repo.full_name,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "releases": repo.get_releases().totalCount,
            "last_updated": repo.updated_at,
            "domain": "python"
        })
    except Exception as e:
        print(f"Error with {name}: {e}")  # Debug: Catch and report the error

# Save to CSV
df = pd.DataFrame(repo_data)
df.to_csv("repository_metadata.csv", index=False)
print("Metadata saved to repository_metadata.csv")