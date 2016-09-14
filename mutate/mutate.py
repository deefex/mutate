# Standard Imports
import argparse
import ast
import os
import sys
import time

# Third Party Imports

# Local Imports
from ast_visitor import AstVisitor
from logger import initialise_logger, print_and_log
from utils import compile_to_file, extract_file_name, get_file_as_string, rename_file, run_unit_tests, \
    unit_test_failures


def mutation_tester(file_under_test, unit_test_suite, mutation_log_file):

    # Construct command for running pytest
    pytest_command = 'py.test -v ' + unit_test_suite

    # Set the log file path/name (should be OS independent)
    if not os.path.exists('logs'):
        os.mkdir('logs')
    if mutation_log_file is not None:
        log_file = os.path.join('logs', mutation_log_file)
    else:
        log_file = os.path.join('logs', extract_file_name(file_under_test).replace('.py', '.log'))

    logger = initialise_logger(log_file)

    print_and_log(logger, 'Mutation Tester Run      : %s' % str(time.strftime("%d-%m-%Y %H:%M")))
    print_and_log(logger, 'File Under Test          : %s' % file_under_test)
    print_and_log(logger, 'Compiled File Under Test : %s' % file_under_test.replace('.py', '.pyc'))
    print_and_log(logger, 'Unit Test Suite          : %s' % unit_test_suite)
    print_and_log(logger, 'Log File                 : %s' % log_file)

    sample_source = get_file_as_string(file_under_test)

    initial_tree = ast.parse(sample_source)
    compiled = compile(initial_tree, '<ast>', 'exec')
    compile_to_file(filename=file_under_test.replace('.py', '.pyc'), compiled_code=compiled)

    original_pass = run_unit_tests(pytest_command, logger)

    file_under_test_backup = file_under_test.replace(".py", ".txt")

    ast_visitor = AstVisitor(filename=file_under_test)

    if original_pass:
        print_and_log(logger, 'Original tests passed, commencing mutations')
    else:
        print_and_log(logger, 'Original test failed, exiting\n')
        quit()

    rename_file(file_under_test, file_under_test_backup)

    mutant_count = 0
    for mutator in ast_visitor.mutators:
        mutant_count += mutator.mutations_count()

    print_and_log(logger, '{0} mutant{1} generated (s denotes survived, k denotes killed)\n'.format(mutant_count, 's' if mutant_count != 1 else ''))

    killed = 0
    survived = 0
    for mutator in ast_visitor.mutators:
        for x in range(0, mutator.mutations_count()):
            mutator.mutate(x)
            compiled = compile(ast_visitor.initial_tree, '<ast>', 'exec')

            compile_to_file(file_under_test.replace('.py', '.pyc'), compiled)

            failures = unit_test_failures(pytest_command)
            if not failures:
                survived += 1
                logger.info('-' * 50 + '\n' + "Mutant SURVIVED\n" + '-' * 50)
                mutator.log_mutant(file_under_test, logger)
                sys.stdout.write('s')
                logger.info('\n')
            else:
                killed += 1
                logger.info('-' * 50 + '\n' + "Mutant KILLED\n" + '-' * 50)
                mutator.log_mutant(file_under_test, logger)
                sys.stdout.write('k')
                logger.info(failures)
        mutator.reset()

    if mutant_count != 0:
        print_and_log(logger, '\n\n' + '-' * 50)
        print_and_log(logger, 'Mutants survived         : {0}/{1}'.format(survived, mutant_count))
        print_and_log(logger, 'Mutants killed           : {0}/{1}'.format(killed, mutant_count))
        print_and_log(logger, 'Mutant kill rate         : {0}%'.format(int(float(killed * 100) / float(mutant_count))))
        print_and_log(logger, '-' * 50)
    else:
        print_and_log(logger, 'No mutants generated')

    rename_file(file_under_test_backup, file_under_test)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", dest="file_under_test", help="path to source file", metavar="FILE")
    parser.add_argument("-t", "--test", dest="unit_test_suite", help="path to unit test file", metavar="FILE")
    parser.add_argument("-l", "--log", dest="mutation_log_file", help="mutation log file name", metavar="FILE")
    args = parser.parse_args()

    suffix = ".py"
    if (args.file_under_test is not None) and (args.unit_test_suite is not None):
        if os.path.exists(args.file_under_test) and os.path.exists(args.unit_test_suite):
            if args.file_under_test.endswith(suffix) and args.unit_test_suite.endswith(suffix):
                mutation_tester(args.file_under_test, args.unit_test_suite, args.mutation_log_file)
            else:
                print "Mutation Test Aborted: One or both of the file arguments isn't a python file"
        else:
            print "Mutation Test Aborted: One or both of the file arguments doesn't exist"
    else:
        print "Mutation Test Aborted: One or both of the file arguments are missing"

if __name__ == "__main__":
    main()
