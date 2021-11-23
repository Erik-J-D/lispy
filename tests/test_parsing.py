from lispy import tokenize


def test_tokenize():
    assert tokenize("5") == [5]

    assert tokenize("(1 #t 3)") == [b'(', 1, True, 3, b')']

    assert tokenize("(+ 1 2)") == [b'(', b'+', 1, 2, b')']

    assert tokenize("(+ 1 (+ 1 1))") == [
        b'(', b'+', 1, b'(', b'+', 1, 1, b')', b')']

    assert tokenize('(print "hello"      \t "world" 5)') == [
        b'(', b'print', 'hello', 'world', 5, b')']

    assert tokenize('(print "(hello)" "world" 5)') == [
        b'(', b'print', '(hello)', 'world', 5, b')']

    assert tokenize(r'(print "My name is \"lisp\"")') == [
        b'(', b'print', 'My name is "lisp"', b')']

    assert tokenize('(print "hello" ; ignore this comment\n"world" 5)') == [
        b'(', b'print', 'hello', 'world', 5, b')']
