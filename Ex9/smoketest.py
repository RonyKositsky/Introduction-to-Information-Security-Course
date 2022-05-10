import contextlib
import os
import infosec.core as utils
from infosec import core


@contextlib.contextmanager
def question_context(name):
    try:
        core.smoke.highlight(name)
        yield
    except Exception as e:
        core.smoke.error(e)
    finally:
        # Add a new-line after each question
        print()

def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with question_context("Question 1a"):
        utils.smoke.check_if_nonempty('q1/q1a.py')
        utils.smoke.check_if_nonempty('q1/q1a.txt')
    with question_context("Question 1b"):
        utils.smoke.check_if_nonempty('q1/q1b.py')
        utils.smoke.check_if_nonempty('q1/q1b.txt')
    with question_context("Question 1c"):
        utils.smoke.check_if_nonempty('q1/q1c.txt')
    with question_context("Question 1d"):
        utils.smoke.check_if_nonempty('q1/q1d.py')
        utils.smoke.check_if_nonempty('q1/q1d.txt')
    with question_context("Question 2a"):
        utils.smoke.check_if_nonempty('q2/a/bigbrother.py')
        utils.smoke.check_if_nonempty('q2/a/q2a.txt')
        utils.smoke.check_if_nonempty('q2/b/winston.py')
        utils.smoke.check_if_nonempty('q2/b/julia.py')
    with question_context("Question 2b"):
        utils.smoke.check_if_nonempty('q2/b/q2b.txt')
        utils.smoke.check_if_nonempty('q2/c/bigbrother.py')
    with question_context("Question 2c"):
        utils.smoke.check_if_nonempty('q2/c/q2c.txt')
        utils.smoke.check_if_nonempty('q2/d/winston.py')
        utils.smoke.check_if_nonempty('q2/d/julia.py')
    with question_context("Question 2d"):
        utils.smoke.check_if_nonempty('q2/d/q2d.txt')


if __name__ == '__main__':
    smoketest()
