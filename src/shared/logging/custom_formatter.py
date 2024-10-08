import colorlog

from os_local import join_paths


class CustomColoredFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        src_path = join_paths("src", "")
        src_index = record.pathname.lower().find(src_path)

        if src_index == -1:
            return ""

        record.pathname = record.pathname[src_index:]

        if hasattr(record, "funcName") and hasattr(record, "module"):
            class_name = record.name
            record.funcName = f"{class_name}.{record.funcName}"

        return super().format(record)
