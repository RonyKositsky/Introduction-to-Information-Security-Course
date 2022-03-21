import contextlib
import os

from infosec import core


def identity(x):
    return x


@core.smoke.smoke_check
def check_buffer_from_function(*args, module_path, function_name, what,
                               ascii_selector, **kwargs):
    try:
        with core.smoke.get_from_module(module_path, function_name) as func:
            result = func(*args, **kwargs)
        result = ascii_selector(result) if ascii_selector else result
    except Exception as e:
        raise core.SmoketestFailure(
            f'Exception generating {what} for {module_path}') from e

    if not isinstance(result, (bytes, bytearray)):
        raise core.SmoketestFailure(
            f'Invalid {what} type for {module_path}: type was {type(result)}, '
            f'expected `bytes` or `bytearray`')

    if ascii_selector and any(c >= 0x80 for c in result):
        raise core.SmoketestFailure(
            f'Your {what} from {module_path} contains non-ascii bytes\n'
            f'{repr(result)}')

    core.smoke.success(f'Generated {what} from {module_path}')


@core.smoke.smoke_check
def check_shellcode(module_path, ascii=False):
    return check_buffer_from_function(
        module_path=module_path,
        function_name='get_shellcode' if not ascii else 'get_ascii_shellcode',
        what='shellcode',
        ascii_selector=identity if ascii else None)


@core.smoke.smoke_check
def check_payload(module_path, ascii=False):
    def ascii_part(s):
        if s[-1] == 0:
            return s[4:-5]
        else:
            return s[4:-4]
    return check_buffer_from_function(
        module_path=module_path,
        function_name='get_payload',
        what='payload',
        ascii_selector=ascii_part if ascii else None)


@core.smoke.smoke_check
def check_encode(module_path):
    return check_buffer_from_function(
        module_path=module_path,
        function_name='encode',
        what='encoding',
        ascii_selector=lambda result: result[0],
        data=bytes(range(128, 232)))


@core.smoke.smoke_check
def check_get_decoder(module_path):
    return check_buffer_from_function(
        module_path=module_path,
        function_name='get_decoder_code',
        what='decoder',
        ascii_selector=identity,
        indices=[0, 1, 6, 127])


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
        core.smoke.check_if_nonempty('q1.txt')
        core.smoke.check_if_nonempty('q1.py')
        check_payload('q1.py')

    with question_context('Question 2'):
        core.smoke.check_if_nonempty('shellcode.asm')
        core.smoke.check_if_nonempty('q2.py')
        core.smoke.check_if_nonempty('q2.txt')
        check_payload('q2.py')
        check_shellcode('q2.py')
    
    with question_context('Question 3'):
        core.smoke.check_if_nonempty('q3.txt')
        core.smoke.check_if_nonempty('q3.py')
        check_encode('q3.py')
        check_get_decoder('q3.py')
        check_payload('q3.py', ascii=True)
        check_shellcode('q3.py', ascii=True)


if __name__ == '__main__':
    smoketest()
