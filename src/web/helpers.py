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
