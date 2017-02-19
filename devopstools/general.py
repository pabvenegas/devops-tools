import os
import subprocess
import sys
import yaml

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
            try:
                exec_output = subprocess.check_output(commands, env=os.environ)
            except subprocess.CalledProcessError as ex:
                exec_output = ""
            return exec_output
    except KeyboardInterrupt:
        pass

def load_yaml_file(filepath):
    """ Load yaml file """
    loaded_yaml = None
    if os.path.exists(filepath):
        with open(filepath) as f:
            loaded_yaml = yaml.safe_load(f)

    return loaded_yaml

def write_yaml_file(loaded_yaml, filepath, default_flow_style=False):
    """ Write yaml to file """
    with open(filepath, 'w') as outfile:
        yaml.dump(loaded_yaml, outfile, default_flow_style=default_flow_style)
