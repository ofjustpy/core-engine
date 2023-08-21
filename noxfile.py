import os
from pathlib import Path
import tempfile
import nox

locations = "src",


@nox.session(python=["3.10", "3.11"])
def lint(session):
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    session.run("flake8", *args)


# noxfile.py
@nox.session(python=["3.11"])
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


# noxfile.py
@nox.session(python=["3.11"])
def reorder_imports(session):
    args = session.posargs or locations
    session.install("reorder-python-imports")
    # run reorder on each python file
    files = []
    for location in locations:
        p = Path(location)
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            files.extend(p.rglob("*.py"))

    for file in files:
        session.run("reorder-python-imports", str(file))


@nox.session(python="3.11")
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "bash",
            "-c",
            f"pipenv requirements >  {requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")
