import os, json, subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))

def make(filename, lang):
    makefile_dir = os.path.join(current_dir, "..")
    command = f"make {lang} FILE={filename}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=makefile_dir)
    output, error = process.communicate()
    if error:
        print(error)
        return None
    else:
        print(output)
        return 0
    