import uuid
import os
from background_task import background
from mainApp.models import SolvePost
from datetime import datetime
from .judge_settings import *

# 백그라운드 채점 시스템
@background
def activate_judge():
    waits = SolvePost.objects.filter(result=3) # get all waiting submissions

    for submit in waits:
        try:
            # get problem info
            problem_number = submit.problem_pk.pk
            time_limit = submit.problem_pk.time_limit

            # generate source file name
            while True:
                id = str(uuid.uuid4())
                file_path = os.path.join(CODE_SAVING_DIRECTORY, id)
                if not os.path.exists(file_path): break

            # write source file
            with open(file_path, "w", encoding="utf-8") as code_file:
                code_file.write(submit.body)

            # execute judge script
            if submit.lang == 1:
                exec_path = os.path.join(JUDGE_DOCKER_DIRECTORY, "python3", "exec.sh")
            else:
                raise ValueError("Not Supported Language")

            input_testcase = os.path.join(JUDGE_TESTCASE_DIRECTORY, "%d/%d.in" % (problem_number, 1))
            output_testcase = os.path.join(JUDGE_TESTCASE_DIRECTORY, "%d/%d.out" % (problem_number, 1))
            result = os.system("%s %s %s %s %d" % (exec_path, file_path, input_testcase, output_testcase, time_limit))

            try:
                os.remove(file_path)
            except Exception as e:
                print("[Remove Exception]")
                print("file : " + file_path)
                print(str(e))

            # return value 0 : Accepted, save result
            if result == 0:
                submit.result = 1
            else:
                submit.result = 2
            submit.save()

        except Exception as e:
            # if exception, go to next submission
            print(str(e))
            continue
