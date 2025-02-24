from github import Github
import pandas as pd

# Authenticate with GitHub API
g = Github("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")  # Replace with your actual token

# List of repositories (same as previous steps)
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

# Initialize list to store release data
release_data = []

# Fetch release history for each repository
for name in repo_names:
    try:
        print(f"Processing releases for {name}...")  # Debug output
        repo = g.get_repo(name)
        releases = list(repo.get_releases())  # Convert to list to process all releases
        
        if len(releases) < 2:  # Need at least 2 releases to calculate an interval
            print(f"Skipping {name}: Only {len(releases)} releases found")
            continue
        
        # Get release creation dates (sorted descending by default)
        release_dates = [release.created_at for release in releases]
        # Calculate intervals (note: releases are newest first, so reverse order for chronological intervals)
        release_intervals = [(release_dates[i] - release_dates[i+1]).days 
                             for i in range(len(release_dates)-1)]
        
        # Store data (using index as release_id)
        for i, interval in enumerate(release_intervals):
            release_data.append({
                "repo": name,
                "release_id": i + 1,  # Start from 1
                "release_date": release_dates[i+1],  # Use the later date of the pair
                "interval_days": interval
            })
    except Exception as e:
        print(f"Error with {name}: {e}")  # Catch and report errors

# Save to CSV
df_releases = pd.DataFrame(release_data)
df_releases.to_csv("release_data.csv", index=False)
print("Release data saved to release_data.csv")