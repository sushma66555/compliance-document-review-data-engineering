"""
Shared SentenceTransformer Model for Data Engineering Retrieval Services.

Ensures exactly ONE instance of the SentenceTransformer model is loaded into memory
and shared across all retrieval modules (rule lookup, disclosure check, precedent search).

Thread-safe singleton within a process.
"""

import threading
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

_model = None
_lock = threading.Lock()


def get_shared_model() -> SentenceTransformer:
    """
    Returns the singleton SentenceTransformer instance.
    Loads the model on first access in a thread-safe manner.
    """
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                _model = SentenceTransformer(MODEL_NAME)
    return _model


# Module-level convenience reference (calls get_shared_model on first use)
class _SharedModelProxy:
    """Proxy object that defers model loading until first attribute access."""
    def __getattr__(self, name):
        real_model = get_shared_model()
        return getattr(real_model, name)


model = _SharedModelProxy()
