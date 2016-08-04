import marshal
import ntpath
import os
import py_compile
import subprocess
import time
import shlex
import platform

from logger import print_and_log

def extract_fut_name(path):
    '''
    Use ntpath to extract the fut (file under test) name from the path string.
    Better than using split operations with OS dependent chars ('/' or '\')
    '''
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def run_command(command):
    # This conditional was inserted because the Popen command originally failed on the Mac platform.
    # The shlex.split was added, however, while it now worked on Macs it now failed on Windows.
    # Hence the reason for the if-else
    # TODO - Implement a more harmonious way of  doing this across all platforms.
    if platform.system() == 'Windows':
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


def run_unit_tests(pytest_command, logger):
    '''
    Perform an initial run of the unit tests using 'py.test -v'
    '''
    last_line = ''
    for line in run_command(pytest_command):
        last_line = line
    test_result = last_line.replace("=","").strip()
    print_and_log(logger, 'Test Results             : %s\n'%test_result)

    # Simple logic will need to be adapted depending on test runner
    if ('passed' in test_result) and ('failed' not in test_result):
        return True
    else:
        return False

def unit_test_failures(pytest_command):
    '''
    Run the unit tests, but keep a note of the failing tests for killed mutants
    '''
    failures = ""
    for output in run_command(pytest_command):
        if 'FAILED' in output:
            failures = failures + output.split('/')[-1]
    return failures

def get_file_as_string(file_name):

    fo = open(file_name, 'r')
    contents = fo.read()
    fo.close()
    return contents


def write_string_to_file(file_name, contents):
    fo = open(file_name, "w")
    fo.write(contents)
    fo.close()


def append_string_to_file(file_name, contents):
    fo = open(file_name, "a")
    fo.write(contents)
    fo.close()


def delete_file_if_exists(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)


def rename_file(file_name, new_name):
    delete_file_if_exists(new_name)
    os.rename(file_name, new_name)


def compile_to_file(filename, compiled_code):
    delete_file_if_exists(filename)
    with open(filename, 'wb') as fc:
            fc.write('\0\0\0\0')
            py_compile.wr_long(fc, long(time.time()))
            marshal.dump(compiled_code, fc)
            fc.flush()
            fc.seek(0, 0)
            fc.write(py_compile.MAGIC)





