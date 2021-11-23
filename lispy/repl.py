import readline

from lispy import eval_expr, parse

while True:
    inp = input("lispy> ")
    print(eval_expr(parse(inp)))
