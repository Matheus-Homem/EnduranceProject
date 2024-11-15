from src.shared.logger import LoggerInitializer

_logger_initialized = False


def initialize_logger():
    global _logger_initialized
    if not _logger_initialized:
        LoggerInitializer()
        _logger_initialized = True


initialize_logger()
