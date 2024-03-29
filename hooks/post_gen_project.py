"""This module is called after project is created."""

from typing import List

import textwrap
from pathlib import Path
from shutil import move, rmtree

# Project root directory
PROJECT_DIRECTORY = Path.cwd().absolute()
PROJECT_NAME = "{{ cookiecutter.project_name }}"
PROJECT_MODULE = "{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}"
CREATE_EXAMPLE_TEMPLATE = "{{ cookiecutter.create_example_template }}"

# Values to generate correct license
LICENSE = "{{ cookiecutter.license }}"
ORGANIZATION = "{{ cookiecutter.organization }}"

# Values to generate github repository
GITHUB_USER = "{{ cookiecutter.github_name }}"

licences_dict = {
    "MIT": "mit",
    "BSD-3": "bsd3",
    "GNU GPL v3.0": "gpl3",
    "Apache Software License 2.0": "apache",
}


def generate_license(directory: Path, licence: str) -> None:
    """Generate license file for the project.

    Args:
        directory: path to the project directory
        licence: chosen licence
    """
    move(str(directory / "_licences" / f"{licence}.txt"), str(directory / "LICENSE"))
    rmtree(str(directory / "_licences"))


def remove_unused_files(directory: Path, module_name: str, need_to_remove_cli: bool) -> None:
    """Remove unused files.

    Args:
        directory: path to the project directory
        module_name: project module name
        need_to_remove_cli: flag for removing CLI related files
    """
    files_to_delete: List[Path] = []

    def _cli_specific_files() -> List[Path]:
        return [directory / module_name / "__main__.py"]

    if need_to_remove_cli:
        files_to_delete.extend(_cli_specific_files())

    for path in files_to_delete:
        path.unlink()


def print_further_instuctions(project_name: str, github: str) -> None:
    """Show user what to do next after project creation.

    Args:
        project_name: current project name
        github: GitHub username
    """
    message = f"""
    Your project {project_name} is created.

    1) Now you can start working on it:

        $ cd {project_name} && git init

    2) If you don't have Poetry installed run:

        $ make poetry-download

    3) Initialize poetry and install pre-commit hooks:
        $ venv_create python3.x
        $ make install

    4) Run codestyle:

        $ make codestyle

    5) Upload initial code to GitHub via SSH:
        `make ga-initial` runs:
        $ git add .
        $ git commit -m ":tada: Initial commit"
        $ git branch -M master
        $ git remote add origin git@github.com:$(GITHUB)/$(PROJECT_NAME).git
        $ git push -u origin master

    6) Install pre-commit hooks:
        $ make pre-commit-install

    7) Additional steps:
        1. Setup github-repo-stats
           a. create a new token (done - in vault)
           b. set repository secret: GHRS_GITHUB_API_TOKEN: <API token that has the repo scope>
           c. use _make/upload_repo_secret.py in scriptomatix
        2. Go to deepsource & check project has been activated
        3. Add unique DEEPSOURCE_DSN_SECRET to repository secrets (for coverage)
           a. use make gen-reposecrets DSN=https://xxxx@app.deepsource.com

        4. Run 1-3 using `make gen-reposecrets DSN=$(DSN)`
        #
        5. Update Github repo settings with `make mod-reposettings`:
            a. Only allow squash merging (disable merge & rebase)
            b. Set squash merge to "Pull request title & description"
            c. Automatically delete head branches
            d. Protect master branch:
                i. Require pull request reviews before merging
                ii. Require approvals (1)
                iii. Dismiss stale pull request approvals when new commits are pushed
                iv. Require review from Code Owners
                v. Restrict who can dismiss pull request reviews (i.e. DPArts)
                vi. Allow specified actors to bypass required pull requests (i.e. DPArts)
                vii. other options unchecked
        6. Update pyproject.toml
        7. Update README.md

    """
    print(textwrap.dedent(message))


def main() -> None:
    generate_license(directory=PROJECT_DIRECTORY, licence=licences_dict[LICENSE])
    remove_unused_files(
        directory=PROJECT_DIRECTORY,
        module_name=PROJECT_MODULE,
        need_to_remove_cli=CREATE_EXAMPLE_TEMPLATE != "cli",
    )
    print_further_instuctions(project_name=PROJECT_NAME, github=GITHUB_USER)


if __name__ == "__main__":
    main()
