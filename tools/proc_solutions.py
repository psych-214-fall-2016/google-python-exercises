""" Make exercises

Process solutions to make Python exercises.
"""

import os
import sys
from glob import glob
from os.path import join as pjoin, basename, isdir, abspath
from subprocess import check_call

COMMAND_PARAMS = {
    'babynames.py': ['baby1990.html', 'baby1992.html', 'baby1994.html'],
    'mimic.py': ['small.txt'],
    'wordcount.py': ['--count', 'small.txt'],
    'copyspecial.py': ['solution'],
    'logpuzzle.py': ['animal_code.google.com'],
}


def find_exercises(exercise_dir):
    soln_dir = pjoin(exercise_dir, 'solution')
    py_files = glob(pjoin(soln_dir, "*.py"))
    return [(pjoin(exercise_dir, basename(py_file)), py_file)
            for py_file in py_files]


def process_solution(solution_contents):
    exercise_contents = []
    for line in solution_contents.splitlines():
        exercise_contents.append(line)
    return ''.join(exercise_contents)


def write_solution(solution_fname, exercise_fname):
    with open(solution_fname, 'rt') as fobj:
        solution = fobj.read()
    exercise = process_solution(solution)
    print(solution_fname)
    return
    with open(exercise_fname, 'wt') as fobj:
        fobj.write(exercise)


def rewrite_exercise_dir(exercise_dir):
    for exercise_fname, solution_fname in find_exercises(exercise_dir):
        write_solution(solution_fname, exercise_fname)


def exercise_sdirs(start_path):
    sdirs = []
    for path in os.listdir(start_path):
        full_path = pjoin(start_path, path)
        if isdir(full_path) and isdir(pjoin(full_path, 'solution')):
            sdirs.append(full_path)
    return sdirs


def check_solutions(exercise_dir):
    for exercise_fname, solution_fname in find_exercises(exercise_dir):
        check_solution(exercise_dir, solution_fname)


def check_solution(exercise_dir, solution_fname):
    print('Checking ' + solution_fname)
    fname = abspath(solution_fname)
    cwd = os.getcwd()
    # Allow for commands that need parameters
    parameters = COMMAND_PARAMS.get(basename(fname), [])
    try:
        os.chdir(exercise_dir)
        check_call([sys.executable, fname] + parameters)
    finally:
        os.chdir(cwd)


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else 'check'
    start_path = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    if command == 'write':
        for exercise_dir in exercise_sdirs(start_path):
            rewrite_exercise_dir(exercise_dir)
    elif command == 'check':
        for exercise_dir in exercise_sdirs(start_path):
            check_solutions(exercise_dir)
    else:
        raise RuntimeError('Invalid command ' + command)


if __name__ == '__main__':
    main()
