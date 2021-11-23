from string import whitespace


def tokenize(s: str):
    tokens = []

    while s:
        # paren
        if s[0] in "()":
            tokens.append(bytes(s[0], "utf-8"))
            s = s[1:]
        # skip whitespace
        elif s[0].isspace():
            s = s[1:]
        # string - grab the whole thing
        elif s[0] == '"':
            string, remainder = read_until(
                s[1:], lambda x: x == '"', delim="\\", must_match=True)
            tokens.append(string)
            s = remainder[1:]
        # comment - grab until newline, then resume
        elif s[0] == ";":
            _, remainder = read_until(s, lambda x: x == "\n")
            s = remainder[1:]
        # grab the current atom
        else:
            string, remainder = read_until(
                s, lambda x: x in "();" + whitespace)
            tokens.append(atom_to_primitive_or_bytes(string))
            s = remainder

    return tokens


def atom_to_primitive_or_bytes(s):
    if s == "#t":
        return True
    if s == "#f":
        return False
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            try:
                return complex(s)
            except ValueError:
                pass

    # if we can't parse a primitive, return it as a symbol
    return bytes(s, "utf-8")


def read_until(seq, match_until, delim=None, must_match=False):
    str_so_far = ""

    while seq:
        if seq[0] == delim:
            str_so_far += seq[1]
            seq = seq[2:]
        elif match_until(seq[0]):
            return str_so_far, seq
        else:
            str_so_far += seq[0]
            seq = seq[1:]

    if must_match:
        raise Exception("couldn't read until the next match")
    else:
        return str_so_far, ""


def tokens_to_exp(tokens: list):
    if not tokens:
        raise Exception("failed to parse")
    next_token = tokens.pop(0)
    if next_token == b"(":
        sub_tokens = []
        while tokens[0] != b")":
            sub_tokens.append(tokens_to_exp(tokens))
        tokens.pop(0)
        return tuple(sub_tokens)
    else:
        return next_token


def parse(s: str):
    return tokens_to_exp(tokenize(s))
