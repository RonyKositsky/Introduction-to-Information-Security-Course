import os
import contextlib

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
    with question_context("Question 1"):
        core.smoke.check_if_nonempty('q1/q1.py')
        core.smoke.check_if_nonempty('q1/q1.txt')
    with question_context("Question 2"):
        core.smoke.check_if_nonempty('q2/q2.py')
        core.smoke.check_if_nonempty('q2/q2.txt')
    with question_context("Question 3"):
        core.smoke.check_if_nonempty('q3/q3.py')
        core.smoke.check_if_nonempty('q3/q3.txt')
    with question_context("Question 4"):
        core.smoke.check_if_nonempty('q4/q4.py')
        core.smoke.check_if_nonempty('q4/q4.txt')
    with question_context("Question 5"):
        core.smoke.check_if_nonempty('q5/q5.py')
        core.smoke.check_if_nonempty('q5/q5.txt')

if __name__ == '__main__':
    smoketest()
