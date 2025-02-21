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

def display_info():
    print("BOJ Auto Checker")
    print("Version 1.0")
    print()
    print("Current filename:", config["filename"])
    print("Current main language:", config["mainLanguage"])
    print("Available Languages: \n", ", ".join(available_lang))
    print()

# TODO
def run(opt):
    return None

def on_exit():
    config["availableLanguages"] = available_lang
    with open(config_path, 'w') as f:
        json.dump(config, f)

def parse():
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
            return run(command[1])
        else:
            return run("a")
    elif command[0] in ["make", "m"]:
        return make(config["filename"], config["mainLanguage"])
    elif command[0] in ["help", "h"]:
        print("Commands:")
        print("  !<command>: Run shell command")
        print("  help, h: Show this message")
        print("  exit, quit, q: Exit the program")
        print("  run, r [a,b,t]: Run the program")
        print("  make, m: Compile the source code")
        print("  setl <lang>: Set the main language")
        print("  setf <filename>: Set the filename")
        print("  info: Display information")
        return
    elif command[0] == "setl":
        if length == 2:
            if command[1] in available_lang:
                config["mainLanguage"] = command[1]
            else:
                print("Invalid language")
                print("Available Languages: \n", *available_lang)
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
            return
    elif command[0] == "info":
        display_info()
        return None
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

problem = input("Problem Number: ")

while (True):
    result = parse()