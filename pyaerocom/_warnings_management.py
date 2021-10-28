from __future__ import annotations

import warnings
from contextlib import contextmanager


@contextmanager
def filter_warnings(apply: bool, categories: list | None = None, messages: list | None = None):
    """
    Decorator that can be used to filter particular warnings

    Parameters
    ----------
    apply : bool
        if True warnings will be filtered, else not.
    categories : list, optional
        list of warning categories to be filtered. E.g.
        [UserWarning, DeprecationWarning]. The default is None. For each
        `<entry>` :func:`warnigns.filterwarnings('ignore', category=<entry>)`
        is called.
    messages : list, optional
        list of warning messages to be filtered. E.g.
        ['Warning that can safely be ignored']. The default is None. For each
        `<entry>` :func:`warnigns.filterwarnings('ignore', message=<entry>)`
        is called.

    Example
    -------
    @filter_warnings(categories=[UserWarning, DeprecationWarning],
                     messages=['I REALLY'])
    def warn_randomly_and_add_numbers(num1, num2):
        warnings.warn(UserWarning('Harmless user warning'))
        warnings.warn(DeprecationWarning('This function is deprecated'))
        warnings.warn(Warning('I REALLY NEED TO REACH YOU'))
        return num1+num2

    """
    if categories is None:
        categories = []
    elif not isinstance(categories, list):
        raise ValueError("categories must be list or None")
    if messages is None:
        messages = []
    elif not isinstance(messages, list):
        raise ValueError("messages must be list or None")

    try:
        with warnings.catch_warnings():
            if apply:
                for cat in categories:
                    warnings.filterwarnings("ignore", category=cat)
                for msg in messages:
                    warnings.filterwarnings("ignore", message=msg)
            yield
    finally:
        pass
