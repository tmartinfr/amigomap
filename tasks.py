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
def test(c):
    """
    Run test suite
    """
    c.run("flake8 -j 1", pty=True)
    c.run("find app/ -name '*.py' | xargs isort --check-only --diff", pty=True)
    c.run("pytest --ds config.settings.base", pty=True)


@task
def openapi(c):
    """
    Generate OpenAPI schema
    """
    c.run("django-admin generateschema --url http://localhost:8000 >openapi.yml")
