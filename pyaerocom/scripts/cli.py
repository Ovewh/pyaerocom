from argparse import ArgumentParser

from pyaerocom import const, tools, __version__


def init_parser():

    ap = ArgumentParser(description="pyaerocom command line interface")

    ap.add_argument("-b", "--browse", help="Browse database")
    ap.add_argument("--clearcache", action="store_true", help="Delete cached data objects")
    ap.add_argument("--ppiaccess", action="store_true", help="Check if MetNO PPI can be accessed")
    ap.add_argument("-V", "--version", help="Installed version of pyaerocom")

    return ap


def confirm():
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


def main():
    ap = init_parser()

    args = ap.parse_args()

    if args.browse:
        print(f"Searching database for matches of {args.browse}")
        print(tools.browse_database(args.browse))

    if args.clearcache:
        print("Are you sure you want to delete all cached data objects?")
        if confirm():
            print("OK then.... here we go!")
            tools.clear_cache()
        else:
            print("Wise decision, pyaerocom will handle it for you automatically anyways ;P")

    if args.ppiaccess:
        print("True") if const.has_access_lustre else print("False")

    if args.version:
        print(__version__)
