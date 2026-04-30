import logging
import json

# one logger for the whole app — no need for per-module instances here
_logger = logging.getLogger("tech-insight-agent")
_logger.setLevel(logging.INFO)

# only add handler if none exist — avoids duplicate logs on warm Lambda starts
if not _logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(handler)


def _emit(level: str, stage: str, message: str, extra: dict = None) -> None:
    # structured JSON keeps CloudWatch logs easy to query and filter
    payload = {"level": level, "stage": stage, "message": message}

    # only attach extras when caller passes something — keeps log lines lean
    if extra:
        payload["extra"] = extra

    log_fn = getattr(_logger, level.lower(), _logger.info)
    log_fn(json.dumps(payload))


def info(stage: str, message: str, extra: dict = None) -> None:
    _emit("INFO", stage, message, extra)


def error(stage: str, message: str, extra: dict = None) -> None:
    _emit("ERROR", stage, message, extra)


def warn(stage: str, message: str, extra: dict = None) -> None:
    _emit("WARNING", stage, message, extra)
