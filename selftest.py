"""Run tests and attempt self-healing on failure."""

import unittest
from selfheal import repair


def run():
    suite = unittest.defaultTestLoader.discover('tests')
    result = unittest.TextTestRunner().run(suite)
    if not result.wasSuccessful():
        repair()
        result = unittest.TextTestRunner().run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    ok = run()
    raise SystemExit(0 if ok else 1)
