from typing import Dict, List


class SimpleMessagePrinter:

    @staticmethod
    def success(text: str) -> None:
        print(f"\033[92mSUCCESS - {text}\033[0m")

    @staticmethod
    def debug(text: str) -> None:
        print(f"\033[95mDEBUG - {text}\033[0m")

    @staticmethod
    def error(text: str) -> None:
        print(f"\033[91mERROR - {text}\033[0m")


def filter_dictionary(dicts: List[Dict[str, str]], by: str, request) -> List[Dict[str, str]]:
    arg = request.args.get(by, None)
    return [dict for dict in dicts if dict[by] == arg] if arg else dicts
