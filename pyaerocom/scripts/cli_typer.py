# from optparse import Option
# from pickle import FALSE
from typing import Optional
from pyaerocom import const, tools

import typer

app = typer.Typer()


def _confirm():
    """
    Ask user to confirm something

    Returns
    -------
    bool
        True if user answers yes, else False
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("[Y/N]? ").lower()
    return answer == "y"


@app.command()
def browse(database: str):
    """Browse database"""
    print(f"Searching database for matches of {database}")
    print(tools.browse_database(database))


@app.command()
def clearcache():
    """Delete cached data objects"""

    print("Are you sure you want to delete all cached data objects?")
    if _confirm():
        print("OK then.... here we go!")
        tools.clear_cache()
    else:
        print("Wise decision, pyaerocom will handle it for you automatically anyways ;P")


@app.command()
def ppiaccess():
    """Check if MetNO PPi can be accessed"""
    print("True") if const.has_access_lustre else print("False")


@app.command()
def version():
    """Installed version of pyaerocom"""
    from pyaerocom import __version__

    print(__version__)


if __name__ == "__main__":
    app()
