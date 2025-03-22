from github import Github
import pandas as pd

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


release_data = []

for name in repo_names:
    try:
        print(f"Processing releases for {name}...")  
        repo = g.get_repo(name)
        releases = list(repo.get_releases())  
        
        if len(releases) < 2:  
            print(f"Skipping {name}: Only {len(releases)} releases found")
            continue
        
        release_dates = [release.created_at for release in releases]
        release_intervals = [(release_dates[i] - release_dates[i+1]).days 
                             for i in range(len(release_dates)-1)]
        
        for i, interval in enumerate(release_intervals):
            release_data.append({
                "repo": name,
                "release_id": i + 1,  
                "release_date": release_dates[i+1],  
                "interval_days": interval
            })
    except Exception as e:
        print(f"Error with {name}: {e}")  

# Save to CSV
df_releases = pd.DataFrame(release_data)
df_releases.to_csv("release_data.csv", index=False)
print("Release data saved to release_data.csv")