import os, json

current_dir = os.path.dirname(os.path.abspath(__file__))


def get_available_langs():
    result = []
    with open(os.path.join(current_dir, "../Makefile"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.endswith(":\n") and line != "clean:\n":
                result.append(line.split(":")[0])
    return result
