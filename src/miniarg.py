import sys
from typing import Any, Callable, Dict, List, Optional, Union


class Argument:
    """
    Represents a single CLI argument (positional or optional).
    """

    def __init__(
        self,
        name: str,
        *,
        dest: Optional[str] = None,
        required: bool = False,
        default: Any = None,
        type: Callable[[str], Any] = str,
        action: Optional[str] = None,
    ):
        self.name: str = name
        self.dest: str = dest or name.lstrip("-")
        self.required: bool = required
        self.default: Any = default
        self.type: Callable[[str], Any] = type
        self.action: Optional[str] = action  # e.g. "store_true"


class ArgParser:
    """
    Supports:
    - optional and positional arguments
    - type conversion
    - default values
    - 'store_true' boolean flags
    """

    def __init__(self) -> None:
        self.optionals: Dict[str, Argument] = {}
        self.positionals: List[Argument] = []

    def add_argument(self, name: str, **kwargs: Any) -> None:
        """
        Adds a new argument definition.

        Parameters:
        - name: argument name (e.g., "--csv" or "folder")
        - kwargs: supported keys are dest, required, default, type, action
        """
        arg = Argument(name, **kwargs)
        if name.startswith("-"):
            self.optionals[name] = arg
        else:
            self.positionals.append(arg)

    def parse_args(self, argv: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Parses the given list of CLI arguments and returns a dictionary.

        Parameters:
        - argv: Optional argument list (defaults to sys.argv[1:])

        Returns:
        - dict with keys corresponding to argument destinations and parsed values
        """
        argv = argv or sys.argv[1:]
        result: Dict[str, Any] = {}
        pos_index = 0
        i = 0

        while i < len(argv):
            token = argv[i]

            if token in self.optionals:
                arg = self.optionals[token]
                if arg.action == "store_true":
                    result[arg.dest] = True
                    i += 1
                else:
                    i += 1
                    if i >= len(argv):
                        raise ValueError(f"Missing value for {token}")
                    result[arg.dest] = arg.type(argv[i])
                    i += 1

            else:
                if pos_index >= len(self.positionals):
                    raise ValueError(f"Unexpected positional argument: {token}")
                arg = self.positionals[pos_index]
                result[arg.dest] = arg.type(token)
                pos_index += 1
                i += 1

        for arg in self.optionals.values():
            if arg.dest not in result:
                result[arg.dest] = arg.default if arg.action != "store_true" else False

        for arg in self.positionals[pos_index:]:
            if arg.required:
                raise ValueError(f"Missing required positional argument: {arg.name}")
            result[arg.dest] = arg.default

        return result
