"""Compatibility imports for the archived v1 fixture contract."""

from .inference import InferenceInstance as Task
from .inference import prediction_error, rank_files, valid_path
from .metrics import evaluate, summarize

__all__ = ["Task", "prediction_error", "rank_files", "valid_path", "evaluate", "summarize"]
