import os
import subprocess
import sys

def execute(command):

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

    output = process.communicate()[0]
    exit_code = process.returncode

    return (exit_code, output)

def exec_command(commands, realtime_output=False):
    """
    Exec command
    """
    try:
        if realtime_output:
            (return_code, output) = execute(commands)
            return output
        else:
            exec_output = subprocess.check_output(commands, env=os.environ)
            return exec_output
    except KeyboardInterrupt:
        pass

