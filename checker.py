from modules import *
import sys, os, atexit, readline
import subprocess
import json


current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "config.json")

with open(config_path, 'r') as f:
    config = json.load(f)

available_lang = get_available_langs()
config["availableLanguages"] = available_lang

def display_info(prob=0):
    print("BOJ Auto Checker")
    print("Version 1.1.2")
    print()
    if prob:
        print("Current Problem Number:", prob)
    print("Current filename:", config["filename"])
    print("Current main language:", config["mainLanguage"])
    print("Available Languages: \n", ", ".join(available_lang))
    print()

def run(opt, prob : Problem):
    result = []
    if opt == "a":
        print("Testing BOJ + testcase.ac\n")
        for i in range(prob.cases):
            result.append(run_case(config["filename"], i+1, prob.testcases[i], prob.answers[i], prob.time_limit, config["mainLanguage"]))
        print()
        print("BOJ Results:")
        for i in range(prob.cases):
            print(f"Case {i+1}: {'Pass' if result[i] else 'Fail'}")
        print()
        run_ac(prob.prob_num, config["filename"], config["mainLanguage"], prob.ac)
    elif opt == "b":
        print("Testing BOJ\n")
        for i in range(prob.cases):
            result.append(run_case(config["filename"], i+1, prob.testcases[i], prob.answers[i], prob.time_limit, config["mainLanguage"]))
        print()
        print("BOJ Results:")
        for i in range(prob.cases):
            print(f"Case {i+1}: {'Pass' if result[i] else 'Fail'}")
    elif opt == "t":
        print("Testing testcase.ac\n")
        run_ac(prob.prob_num, config["filename"], config["mainLanguage"], prob.ac)
    elif opt == "g":
        print("Debug mode, Testing BOJ\n")
        for i in range(prob.cases):
            run_case(config["filename"], i+1, prob.testcases[i], prob.answers[i], prob.time_limit, config["mainLanguage"], True)
    else:
        print("Invalid option")
        print("Usage: run [a,b,t,g]")
        print("a: Run both BOJ and testcase.ac (default), b: Run only BOJ, t: Run only testcase.ac, g: Debug mode, no grading")
        return None
    return 0
    
def on_exit():
    config["availableLanguages"] = available_lang
    with open(config_path, 'w') as f:
        json.dump(config, f)

def parse(prob : Problem):
    command = input(">> ").split()
    length = len(command)
    if length == 0:
        return None
    if command[0].startswith('!'):
        command[0] = command[0][1:]
        commands = ' '.join(command).split('|')
        processes = []
        try:
            for cmd in commands:
                cmd = cmd.strip().split()
                if processes:
                    processes.append(subprocess.Popen(cmd, stdin=processes[-1].stdout, stdout=subprocess.PIPE, text=True))
                    processes[-2].stdout.close()
                else:
                    processes.append(subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True))
            output, _ = processes[-1].communicate()
            print(output)
            return 0
        except Exception as e:
            command = ' '.join(command)
            print(f"failed to execute: {command}")
            return None
    elif command[0] in ["run", "r"]:
        if length > 1:
            return run(command[1], prob)
        else:
            return run("a", prob)
    elif command[0] in ["make", "m"]:
        return make(config["filename"], config["mainLanguage"])
    elif command[0] == "clean":
        return make(config["filename"],"clean")
    elif command[0] in ["help", "h"]:
        print("Commands:")
        print("  !<command>: Run shell command")
        print("  help, h: Show this message")
        print("  exit, quit, q: Exit the program")
        print("  run, r [a,b,t,g]: Run your code")
        print("  make, m: Compile the source code")
        print("  clean: Remove compiled files")
        print("  setl <lang>: Set the main language")
        print("  setf <filename>: Set the filename")
        print("  info: Display checker information")
        print("  prob: Display problem information")
        print("  showex, ex, se: Show testcases")
        return
    elif command[0] == "setl":
        if length == 2:
            if command[1] in available_lang:
                config["mainLanguage"] = command[1]
            else:
                print("Invalid language")
                print("Available Languages:\n", *available_lang)
            return 0
        else:
            print("Usage: setl <language>")
            return None
    elif command[0] == "setf":
        if length == 2:
            config["filename"] = command[1]
            return 0
        else:
            print("Usage: setf <filename>")
            return None
    elif command[0] == "info":
        display_info(prob.prob_num)
        return 0
    elif command[0] == "prob":
        print("Current Problem Number:", prob.prob_num)
        print("Title:", prob.title)
        print("Level:", prob.level)
        print("Time Limit:", prob.time_limit, "sec")
        print("Memory Limit:", prob.mem_limit)
        print("Avg Tries:", prob.avg_tries)
        print("Success Count:", prob.success_cnt)
        print("# Cases:", prob.cases)
        print("testcase.ac available:", prob.ac)
        print()
        return 0
    elif command[0] in ["showex","ex","se"]:
        for i in range(prob.cases):
            print(f"Case {i+1}:\nInput:\n{prob.testcases[i]}\nOutput:\n{prob.answers[i].strip()}")
            print("-----------------------------------")
        return 0
    elif command[0] in ["exit", "quit", "q"]:
        sys.exit(0)
    else:
        print("Invalid command")
        return None

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')
readline.parse_and_bind('"\e[A": history-search-backward')
readline.parse_and_bind('"\e[B": history-search-forward')
atexit.register(on_exit)

display_info()

while (True):
    try:
        problem = int(input("Problem Number: "))
        if problem < 1000:
            print("Invalid problem number\n")
            continue
    except ValueError:
        print("Invalid problem number\n")
        continue
    break

prob = get_problem(problem)

if (prob is None):
    sys.exit(1)

while (True):
    result = parse(prob)