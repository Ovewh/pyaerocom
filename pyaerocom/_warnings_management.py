from __future__ import annotations

import warnings
from contextlib import contextmanager
from typing import Type


@contextmanager
def ignore_warnings(apply: bool, category: Type[Warning], *messages: str):
    """
    Ignore particular warnings with a decorator or context manager

    Parameters
    ----------
    apply : bool
        if True warnings will be ignored, else not.
    category : subclass of Warning
        warning category to be ignored. E.g. UserWarning, DeprecationWarning.
        The default is Warning.
    *messages : str, optional
        warning messages to be ignored. E.g.
        ignore_warnings(True, Warning, 'Warning that can safely be ignored', 'Other warning to ignore').
        For each
        `<entry>` :func:`warnigns.filterwarnings('ignore', Warning, message=<entry>)`
        is called.

    Example
    -------
    @ignore_warnings(True, UserWarning)
    @ignore_warnings(True, DeprecationWarning)
    @ignore_warnings(True, Warning, 'I REALLY')
    def warn_randomly_and_add_numbers(num1, num2):
        warnings.warn(UserWarning('Harmless user warning'))
        warnings.warn(DeprecationWarning('This function is deprecated'))
        warnings.warn(Warning('I REALLY NEED TO REACH YOU'))
        return num1+num2

    """
    if not issubclass(category, Warning):
        raise ValueError("category must be a Warning subclass")

    if not messages:
        message = ""
    elif all(type(msg) == str for msg in messages):
        message = "|".join(messages)
    else:
        raise ValueError("messages must be list of strings")

    try:
        if not apply:
            yield
            return
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=category, message=message)
            yield
    finally:
        pass
