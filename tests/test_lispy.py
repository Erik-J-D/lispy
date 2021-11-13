import pytest  # type: ignore

from lispy import eval_expr


def test_fail():
    with pytest.raises(NotImplementedError):
        eval_expr(())


def test_primitive():
    assert eval_expr(5) == 5
    assert eval_expr(5.8) == 5.8
    assert eval_expr((b"complex", 2.4, 3.2)) == complex(2.4, 3.2)
    assert eval_expr(True) is True
    assert eval_expr("test") == "test"


def test_if_and_comparison():
    assert eval_expr((b"if", (b">", 5, 4), True, False))
    assert eval_expr((b"if", (b"<", 5, 4), False, True))


def test_math():
    assert eval_expr((b"add1", (b"complex", (b"add1", 5), 9))) == complex(7, 9)
    assert eval_expr((b"mod", (b"+", (b"neg", 5), (b"pow", 2, 6)), 7)) == 3


def test_begin():
    assert eval_expr((b"begin",
                      (b"define", b"a", 5),
                      (b"define", b"b", 6),
                      (b"+", b"a", b"b"))) == 11

    # Make sure begin create a new scope
    with pytest.raises(KeyError):
        eval_expr((b"begin",
                   (b"begin",
                       (b"define", b"a", 5)),
                   (b"add1", b"a")))  # b"a" shouldn't be available here


def test_apply():
    assert eval_expr(
        (b"begin",
            (b"define", b"func", (b"lambda", (b"a", b"b"), (b"+", b"a", b"b"))),
            (b"func", 5, 6))) == 11

    assert eval_expr(
        (b"begin",
            (b"define", b"func", (b"lambda", (b"a", b"b"), (b"+", b"a", b"b"))),
            (b"func", 5, (b"add1", 7)))) == 13

    assert eval_expr(
        (b"begin",
            (b"define", b"func", (b"lambda", (b"a", b"b"), (b"pow", b"a", b"b"))),
            (b"func", (b"if", (b"=", 5, 6), 19.2, 2), (b"add1", 7)))) == 256

    assert eval_expr(((b"lambda", (b"x",), (b"+", b"x", 4)), 5)) == 9


def test_recusion():
    assert eval_expr(
        (b"begin",
            (b"define", b"bad_double", (b"lambda", (b"num",),
                                        (b"if",
                                        (b"<=", b"num", 0),
                                        0,
                                        (b"+", 2, (b"bad_double", (b"sub1", b"num")))))),
            (b"bad_double", 7))) == 14
