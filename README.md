# Lispy

This was written as both an exercise and as an excuse to mess around with the new [pattern matching](https://www.python.org/dev/peps/pep-0636/) introduced in python 3.10. If you find yourself here for whatever reason, I'd recommend the following resources instead of my code:

- [Structure and Interpretation of Computer Programs](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book.html) by Abelson, Sussman & Sussman
- [William Byrd on "The Most Beautiful Program Ever Written"](https://www.youtube.com/watch?v=OyfBQmvr2Hc)
- [(How to Write a (Lisp) Interpreter (in Python))](https://norvig.com/lispy.html) by Peter Norvig
    - And the follow up [(An ((Even Better) Lisp) Interpreter (in Python))](https://norvig.com/lispy2.html)

This code is currently the most similar to Peter Norvigs version, and the name collision is purely accidental (there aren't many ways to combine the names "lisp" and "python"...)

## How to run tests:

```
$ poetry install
$ poetry run pytest
```

Make sure you're running at least python 3.10, otherwise nothing will work.
