import math
import operator as op
from functools import reduce
from typing import Any

from .util import DeepChainMap

Env = dict[bytes, Any]


def default_env() -> Env:
    env = {}

    # Math
    env |= {"+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            "abs": abs,
            "complex": complex,
            "max": max,
            "min": min,
            "mod": op.mod,
            "neg": op.neg,
            "pow": op.pow,
            "round": round}

    # Comparisons
    env |= {"<": op.lt, "<=": op.le, "=": op.eq,
            "!=": op.ne, ">": op.gt, ">=": op.ge, "not": op.not_}

    # List
    env |= {"car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "cons": lambda a, d: (a,) + d,
            "len": len,
            "list": lambda *x: tuple(x),
            "null?": lambda x: x == ()}

    # Other
    env |= {"add1": lambda x: x+1,
            "sub1": lambda x: x-1,
            "and": lambda *x: all(x),
            "or": lambda *x: any(x),
            "print": print,
            "procedure?": callable}

    # Turn all the keys into bytes instead of strings
    return {bytes(k, "utf-8"): v for k, v in env.items()}


def eval_expr(exp, env: Env = default_env()):
    match exp:
        # Primitive types
        case int(n) | float(n) | complex(n) | bool(n) | str(n):
            return n

        # Env stuff
        # Use bytes to represent variable names, they'll be our shitty python
        # symbols because it's cleaner than defining a class that subclasses
        # from str
        case bytes(n):
            return env[n]
        case(b"define", bytes(var), value):
            env[var] = eval_expr(value, env)
            return

        # Language constructs
        case(b"if", p, c, a):
            if eval_expr(p, env):
                return eval_expr(c, env)
            else:
                return eval_expr(a, env)
        case(b"begin", *expr_list) if len(expr_list) > 0:
            sub_env = DeepChainMap({}, env)
            return reduce(lambda _, e: eval_expr(e, sub_env), expr_list, None)
        case(b"lambda", params, body):
            return lambda *args: eval_expr(
                body,
                DeepChainMap(dict(zip(params, args)), env))

        # Last case: evaluate the function
        case(func, *args):
            args_evaled = list(map(lambda a: eval_expr(a, env), args))
            python_func = eval_expr(func, env)
            return python_func(*args_evaled)

        # Fail
        case _:
            raise NotImplementedError(f"Don't know how to handle:\n{exp}")
