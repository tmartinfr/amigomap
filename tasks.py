from invoke import task


@task(default=True)
def help(c):
    """
    Print this help message and exit
    """
    c.run("invoke --list")


@task
def populate(c):
    """
    Prepare and fill development DB with random data
    """
    c.run("django-admin migrate")
    c.run("django-admin app_populate_dev_db")


@task
def run(c):
    """
    Start development server
    """
    c.run("django-admin runserver 0.0.0.0:8000", pty=True)


@task
def sh(c):
    """
    Open Django shell
    """
    c.run("django-admin shell_plus", pty=True)


@task
def flake8(c):
    """
    Check linting
    """
    c.run("flake8 -j 1", pty=True)


@task
def isort(c):
    """
    Check imports
    """
    c.run("find app/ -name '*.py' | xargs isort --check-only --diff", pty=True)


@task
def mypy(c):
    """
    Check type hints
    """
    c.run("mypy --cache-dir=/dev/null --strict app", pty=True)


@task
def pytest(c):
    """
    Run unit tests
    """
    c.run("pytest --ds config.settings.base", pty=True)


@task
def test(c):
    """
    Run all tests
    """
    flake8(c)
    isort(c)
    mypy(c)
    pytest(c)


@task
def openapi(c):
    """
    Generate OpenAPI schema
    """
    c.run("django-admin generateschema --url http://localhost:8000 >openapi.yml")
