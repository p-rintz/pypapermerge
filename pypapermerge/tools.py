from __future__ import annotations


def check_ctype(content_type: str) -> None:
    valid = ['documents', 'folders']
    if content_type not in valid:
        raise ValueError(f'_reverse_list: content_type must be one of {valid}.')
    return None


def check_id(idd: str | list[str] | None) -> bool:
    callerc, callerf = whocalledme()
    if idd is None:
        raise TypeError(f'Received no id from {callerc}.{callerf}.')
    if type(idd) is list:
        raise TypeError(f'Received multiple IDs from {callerc}.{callerf}. It should should only be one.')
    if not len(idd.split('-')) == 5 or not len(idd) == 36:  # type: ignore
        raise ValueError(f'Received wrong ID "{idd}" from {callerc}.{callerf}.')
    return True


def whocalledme() -> tuple[str, str]:
    from inspect import stack
    from sys import modules
    stack2 = stack()[2][0]
    if "pytest" in modules:
        return 'tests', stack2.f_code.co_name
    else:
        return stack2.f_locals['self'].__class__.__name__, stack2.f_code.co_name
