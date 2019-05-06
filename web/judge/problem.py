import os
from .judge_settings import *

def save_testcase(problem_number, input_file, output_file):
    folder = os.path.join(JUDGE_TESTCASE_DIRECTORY, str(problem_number))
    try: os.mkdir(folder)
    except FileExistsError: pass
    with open(os.path.join(folder, "1.in"), "wb") as f:
        for chunk in input_file.chunks():
            f.write(chunk.replace(b"\r", b""))
    with open(os.path.join(folder, "1.out"), "wb") as f:
        for chunk in output_file.chunks():
            f.write(chunk.replace(b"\r", b""))
