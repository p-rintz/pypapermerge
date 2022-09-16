"""Internal functions for the API client to use"""
from __future__ import annotations

from inspect import stack
from sys import modules


def check_ctype(content_type: str) -> None:
    """Check if the content type is either 'documents' or 'folders'"""
    valid = ["documents", "folders"]
    if content_type not in valid:
        raise ValueError(f"_reverse_list: content_type must be one of {valid}.")


def check_id(idd: str | list[str] | None) -> bool:
    """Check if id given is a valid papermerge ID"""
    callerc, callerf = whocalledme()
    if idd is None:
        raise TypeError(f"Received no id from {callerc}.{callerf}.")
    if isinstance(idd, list):
        raise TypeError(
            f"Received multiple IDs from {callerc}.{callerf}. It should should only be one."
        )
    if not len(idd.split("-")) == 5 or not len(idd) == 36:  # type: ignore
        raise ValueError(f'Received wrong ID "{idd}" from {callerc}.{callerf}.')
    return True


def whocalledme() -> tuple[str, str]:
    """Function to return the calling function+class"""
    stack2 = stack()[2][0]
    if "pytest" in modules:
        return "tests", stack2.f_code.co_name
    return stack2.f_locals["self"].__class__.__name__, stack2.f_code.co_name
