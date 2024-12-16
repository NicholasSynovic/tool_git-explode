from os import mkdir
from pathlib import Path
from subprocess import Popen  # nosec
from typing import List

import click
import pygit2
from progress.bar import Bar
from pygit2.repository import Repository


def getGitCommits(repo: Repository) -> List[str]:
    return [commit.id.__str__() for commit in repo.walk(repo.head.target)]


def setupRepo(path: Path, remotePath: Path) -> Repository:
    try:
        mkdir(path=path)
    except FileExistsError:
        pass
    repo: Repository = pygit2.init_repository(path=path)
    try:
        repo.remotes.create("origin", remotePath.__str__())
    except ValueError:
        pass
    return repo


def fetchCommit(repoPath: Path, commit: str) -> int:
    process: Popen[bytes] = Popen(
        args=[
            "git",
            "-C",
            repoPath.__str__(),
            "fetch",
            "--quiet",
            "--depth",
            "1",
            "origin",
            commit,
        ],
        shell=False,
    )  # nosec
    return process.wait()


def checkoutFetch(repoPath: Path) -> int:
    process: Popen[bytes] = Popen(
        args=["git", "-C", repoPath.__str__(), "checkout", "FETCH_HEAD"],
        shell=False,
    )  # nosec
    return process.wait()


@click.command()
@click.option(
    "-r",
    "--repo",
    "repoPath",
    required=True,
    type=click.Path(
        exists=True,
        dir_okay=True,
        readable=True,
        writable=True,
        resolve_path=True,
        path_type=Path,
    ),
    help="Path to git repository",
)
def main(repoPath: Path) -> None:
    repo: Repository = Repository(path=repoPath.__str__())
    commits: List[str] = getGitCommits(repo=repo)

    setupRepo(path=Path("/tmp/ramdisk/hello"), remotePath=repoPath)  # nosec
    fetchCommit(
        repoPath=Path("/tmp/ramdisk/hello"),  # nosec
        commit=commits[10],
    )
    checkoutFetch(repoPath=Path("/tmp/ramdisk/hello"))  # nosec
    quit()

    with Bar(
        "Checking out and cloning repository...",
        max=len(commits),
    ) as bar:
        commit: str
        for commit in commits:
            bar.next()


if __name__ == "__main__":
    main()
