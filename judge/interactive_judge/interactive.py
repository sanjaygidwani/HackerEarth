import subprocess
from .models import Problems
'''
    Returns 0 if the verdict is AC
    Returns 1 if the verdict is WA
    Returns 2 if the verdict is TLE
    Returns 3 if the verdict is CEU - UserCode
    Returns 4 if the veriict is CEI - Interactor
    Returns 5 if there is problem in the judge - SE Server Error
'''
def execute_interactive_testcase_(info):

    sub_id = str(info["sid"])
    problem_obj = Problems.objects.get(pk = int(info['id']))
    user_code = info["path_to_user_sol"]

    pipe1 = sub_id + "pipe1"
    pipe2 = sub_id + "pipe2"
    
    cmd_make_pipes = "mkfifo " + pipe1 + " " + pipe2
    pipe_gen_status = subprocess.call(cmd_make_pipes , shell = True)
    if pipe_gen_status != 0:
        return 5
    
    user_exec = sub_id + "user.out"
    cmd_gen_user_exec = "g++ -std=c++14 " + user_code + " -o " + user_exec
    
    int_exec = sub_id + "interactor.out"
    cmd_gen_interactor_exec = "g++ -std=c++14 " + problem_obj["interactor"] + " -o " + int_exec

    compile_status_user = subprocess.call(cmd_gen_user_exec , shell = True)
    if compile_status_user != 0:
        return 3

    compile_status_interactor = subprocess.call(cmd_gen_interactor_exec , shell = True)
    if compile_status_interactor != 0:
        return 4

    if info["userinputfile"]:
        subprocess.call("cat " + info["userinputfile"] + " >" + pipe2 , shell = True)
    
    if info["interactorinputfile"]:
        subprocess.call("cat " + info["interactorinputfile"] + " >" + pipe1 , shell = True)

    cmd_run_user = "/usr/bin/time --verbose timeout 2 ./" + user_exec + ">" + pipe1 + " <" + pipe2
    cmd_run_interactor = "/usr/bin/time --verbose timeout 2 ./" + int_exec + " <" + pipe1 + " >" + pipe2

    exit_code_interactor = subprocess.Popen(cmd_run_interactor , shell = True)
    exit_code_user = subprocess.Popen(cmd_run_user , shell = True)

    exit_code_interactor = exit_code_interactor.wait()
    exit_code_user = exit_code_user.wait()

    cmd_remove_pipes = "rm " + pipe1 + " " + pipe2
    cmd_remove_executables = "rm " + user_exec + " " +  int_exec
    pipe_remove_status = subprocess.call(cmd_remove_pipes , shell = True)
    if pipe_remove_status != 0:
        return 5
    executables_remove_status = subprocess.call(cmd_remove_executables , shell = True)
    if executables_remove_status != 0:
        return 5

    if exit_code_user == 0:
        return 0
    if exit_code_user == 124:
        return 2
    if exit_code_user == 134:
        return 1

def execute_interactive_testcase(info):
    final_result = {"verdict" : 0 , "time" : 0.6 , "memory" : 1024}
    final_result["verdict"] = execute_interactive_testcase_(info)
    return final_result
