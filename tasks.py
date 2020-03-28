from invoke import task


@task(default=True)
def help(c):
    """
    Print this help message and exit
    """
    c.run("invoke --list")


@task
def populate_dev_db(c):
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
    c.run("flake8 -j 1 --exclude=app/migrations", pty=True)


@task
def isort(c):
    """
    Check imports
    """
    c.run(
        "find app/ -name '*.py' -not -path 'app/migrations*' | \
           xargs isort --check-only --diff",
        pty=True,
    )


@task
def pytest(c):
    """
    Run unit tests
    """
    c.run(
        "pytest --ds config.settings.base "
        "--cov=app --cov-fail-under=100 --no-cov-on-fail",
        pty=True,
    )


@task
def test(c):
    """
    Run all tests
    """
    flake8(c)
    isort(c)
    pytest(c)
