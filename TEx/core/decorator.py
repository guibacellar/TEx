"""Generic Decorators."""

import logging

from functools import wraps
from typing import Callable, Dict, List, Optional, TypeVar, Union

Params = TypeVar('Params')
Return = TypeVar('Return')


def bs4_error_hander(on_error_return_value: Optional[Union[str, List, Dict]] = None) -> Callable:
    """Handle Generic Erros while Acessing the BS4 Object."""

    def inner_bs4_error_hander(func: Callable[[Params], Union[Return, Optional[str]]]) -> Union[Callable, Optional[str]]:
        """Handle Generic Erros while Acessing the BS4 Object."""

        @wraps(func)
        def wrapper(*args: Params, **kwargs: Dict) -> Return:
            """Handle Generic Erros while Acessing the BS4 Object."""
            try:
                return func(*args, **kwargs)  # type: ignore

            except Exception as ex:  # pylint: disable=W0702 # noqa: B901, E722, B001

                logging.error(
                    msg=str(func),
                    exc_info=ex
                    )

                return on_error_return_value  # type: ignore

        return wrapper

    return inner_bs4_error_hander
