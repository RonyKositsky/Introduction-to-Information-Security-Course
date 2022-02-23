import contextlib
import os

from infosec import core
from infosec.core.smoke import success


def compute_number(program_path, value):
    result = core.execute([program_path, str(value)], timeout=10)
    if result.exit_code:
        raise core.SmoketestFailure(f'Program crashes on {value}!')
    try:
        return int(result.stdout.strip())
    except ValueError:
        raise core.SmoketestFailure(
            f'Expected a number as output, got {result.stdout}')


def check_squarebonacci(*sources):
    with core.temporary_directory() as temporary_directory_path:
        target_path = os.path.join(temporary_directory_path, 'q2')
        core.compile_executable(sources=sources, output=target_path)
        values = tuple(compute_number(target_path, i) for i in range(6))
        expected = (0, 1, 1, 2, 5, 29)
        if values != expected:
            raise core.SmoketestFailure(
                f'Squarebonacci sequence from {sources} should begin with '
                f'{", ".join(str(v) for v in expected)}, ... '
                f'not with {", ".join(str(v) for v in values)}, ...')
        success(f'Program for works for some inputs')


def check_exact_sqrt(*sources):
    with core.temporary_directory() as temporary_directory_path:
        target_path = os.path.join(temporary_directory_path, 'q1')
        core.compile_executable(sources=sources, output=target_path)
        inputs = tuple(range(-1, 10))
        expected_results = (0, 0, 1, 0, 0, 2, 0, 0, 0, 0, 3)
        for number, expected in zip(inputs, expected_results):
            result = compute_number(target_path, number)
            if result != expected:
                raise core.SmoketestFailure(
                    f'Exact square-root (from {sources}) of {number} '
                    f'should be {expected}, but computed result was {result}')
        success(f'Program for works for some inputs')


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

    with question_context('Question 1'):
        core.smoke.check_if_nonempty('q1.s')
        check_exact_sqrt('q1.s', 'skeleton.c')

    with question_context('Question 2a'):
        core.smoke.check_if_nonempty('q2a.s')
        check_squarebonacci('q2a.s', 'skeleton.c')

    with question_context('Question 2b'):
        core.smoke.check_if_nonempty('q2b.s')
        check_squarebonacci('q2b.s', 'skeleton.c')

    with question_context('Question 3'):
        core.smoke.check_if_nonempty('q3.txt')


if __name__ == '__main__':
    smoketest()
