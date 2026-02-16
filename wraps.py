#!/usr/bin/python3

from functools import wraps
from timeit import default_timer as timer


def print_time(function):
    @wraps(function)
    def wrapper(*args, **kargs):
        start = timer()
        result = function(*args, **kargs)
        end = timer()
        print("The function {0} Cost {1:3f}s.\n".format(function.__name__, end - start))
        return result

    return wrapper


@print_time
def main():
    print("test")


if __name__ == "__main__":
    main()
