from functools import wraps
from itertools import repeat, zip_longest


def enforce_iterable_state(arg):
    try:
        arg.__iterable__
    except (AttributeError, SyntaxError):
        retval = repeat(arg)
    else:
        if isinstance(arg, str):
            retval = repeat(arg)
        else:
            retval = repeat(arg)

    return retval


def accept_iterables(func, *args, **kwargs):
    _args = [enforce_iterable_state(arg) for arg in args]
    _kwargs = {kn: enforce_iterable_state(kv) for kn, kv in kwargs.items()}
    if _kwargs:
        @wraps(func)
        def wrapper(_args, _kwargs):
            retval = []
            for __args, __kwargs in zip_longest(_args, _kwargs):
                retval.append(func(*__args, **__kwargs))
                if all([isinstance(__arg, repeat) for __arg in __args]) and all([isinstance(kv, repeat) for kv in _kwargs.values()]):
                    break

            return retval
    else:
        @wraps(func)
        def wrapper(_args):
            retval = []
            for __args in _args:
                retval.append(func(*__args))
                if all([isinstance(__arg, repeat) for __arg in __args]):
                    break

            return retval

    return wrapper


@accept_iterables
def plus(x,y):
    return x+y

if __name__ == '__main__':
    print(plus([(0,0), (0,1), (1,1), (1,2), (2,3), (3, 5), (5, 8), (8,13)]))

