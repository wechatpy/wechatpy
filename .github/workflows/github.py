"""
quick script to write mypy errors to github comments
"""
import re
import sys


MYPY_REGEX = r"^(\w:)?(?P<file>[^:]+):(?P<line>\d+):((?P<col>\d+):)?" r"\s*(?P<type>[^:]+):\s*(?P<msg>.+)"
MYPY = re.compile(MYPY_REGEX)


def error(file: str, line: int = 0, col: int = 0, message: str = "error", warn: bool = False) -> None:
    """write an error to stdout"""
    kind = "warning" if warn else "error"
    print(f"::{kind} file={file},line={line},col={col}::{message}")


def main(file_path: str) -> None:
    """read the given file, and print errors"""
    data = ""
    with open(file_path) as file:
        data = file.read()

    for line in data.split("\n"):
        match = MYPY.match(line)
        if match:
            values = match.groupdict()
            error(
                values["file"],
                line=int(values["line"]),
                col=int(values["col"]),
                message=values["msg"],
            )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("you must specify a json file path!")
        sys.exit(1)
    file_path = sys.argv[1]
    main(file_path)
