import marshal
import ntpath
import os
import py_compile
import subprocess
import time
import shlex
import platform

from logger import print_and_log


def extract_file_name(path):
    """ Return a file name from a full path - Much easier to do with ntpath (at least syntactically) """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def run_command(command):
    """ run a single pytest command
    What worked on Windows didn't on anything else and vice-versa - hence the conditional - Grrr. """
    # TODO - There's probably a better way of doing this across all platforms. Investigate.
    if platform.system() == 'Windows':
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


def run_unit_tests(pytest_command, logger):
    """ Perform an initial run of the unit test suite using 'py.test -v' """
    last_line = ''
    for line in run_command(pytest_command):
        last_line = line
    test_result = last_line.replace("=", "").strip()
    print_and_log(logger, 'Test Results             : %s\n' % test_result)

    # Simple logic will need to be adapted depending on test runner
    if ('passed' in test_result) and ('failed' not in test_result):
        return True
    else:
        return False


def unit_test_failures(pytest_command):
    """ Run the unit tests, but keep a note of the failing tests for KILLED mutants """
    failures = ""
    for output in run_command(pytest_command):
        if 'FAILED' in output:
            failures = failures + output.split('/')[-1]
    return failures


def get_file_as_string(file_name):
    """ Take the original source and return it as a string for parsing into the AST """
    fo = open(file_name, 'r')
    contents = fo.read()
    fo.close()
    return contents


def delete_file_if_exists(file_name):
    """ If a file name exists, delete it! Used within the context of renaming files (below) """
    if os.path.isfile(file_name):
        os.remove(file_name)


def rename_file(file_name, new_name):
    """ Used for moving the file_under_test.py to file_under_test.txt and vice-versa before/after mutation """
    delete_file_if_exists(new_name)
    os.rename(file_name, new_name)


def compile_to_file(filename, compiled_code):
    """ Compile the file_under_test.py to its .pyc form - ensuring consistency before and between mutations """
    # TODO - Investigate whether
    delete_file_if_exists(filename)
    with open(filename, 'wb') as fc:
            fc.write('\0\0\0\0')
            py_compile.wr_long(fc, long(time.time()))
            marshal.dump(compiled_code, fc)
            fc.flush()
            fc.seek(0, 0)
            fc.write(py_compile.MAGIC)
