from src.miniarg import ArgParser
from src.check import Check


def parse_args(argv: list[str] = None) -> dict:
    parser = ArgParser()

    parser.add_argument("--mode", default="bench", type=str)
    parser.add_argument("--config", default="default.cfg", type=str)
    parser.add_argument("--csv", default="test_results.csv", type=str)
    parser.add_argument("--template", default=None, type=str)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("folder", type=str)

    args = parser.parse_args(argv)
    Check.value_in(args["mode"], {"bench", "plot", "template"})

    return args
