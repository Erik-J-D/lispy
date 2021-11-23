import readline
from sys import exit

from lispy import eval_expr, parse

while True:
    try:
        inp = input("lispy> ")
        if inp == "exit":
            raise EOFError
        print(eval_expr(parse(inp)))
    except (EOFError, KeyboardInterrupt):  # raised by ctrl-d / ctrl-c
        exit("Goodbye")
    except Exception as e:
        print("ERROR:", e)
