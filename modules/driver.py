import os, subprocess, psutil
import json
import requests
from .loader import get_testac_id, get_code
from threading import Thread

current_dir = os.path.dirname(os.path.abspath(__file__))

def make(filename: str, lang: str) -> int | None:
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
    

def run_case(filename : str, num : int, testcase : str, ans : str, timelimit : float, lang : str, debug : bool = False) -> bool:
    class ThreadFlag:
        def __init__(self):
            self._flag = False
        def set(self):
            self._flag = True
        def is_set(self):
            return self._flag
    
    def monitor_memory(proc, result, stop_flag):
        max_memory = 0
        while not stop_flag.is_set():
            try:
                total_memory = proc.memory_info().rss
                for child in proc.children(recursive=True):
                    total_memory += child.memory_info().rss
                max_memory = max(max_memory, total_memory)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break
        result.append(max_memory)

    success = False
    print(f"Running case {num}...")
    cmd = [os.path.join(current_dir, f"../../{filename}")]
    if lang.count("py"):
        timelimit = timelimit * 3 + 2
        cmd[0] += ".py"
        cmd = ["python3"] + cmd
    elif lang.count("java"):
        timelimit = timelimit * 2 + 1
        cmd[0] += ".java"
        cmd = ["java"] + cmd
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    ps_process = psutil.Process(process.pid)

    memory = []
    stop_flag = ThreadFlag()
    monitor_thread = Thread(target=monitor_memory, args=(ps_process, memory, stop_flag))
    monitor_thread.start()
    try:
        result = process.communicate(input=testcase, timeout=timelimit)
    except subprocess.TimeoutExpired:
        process.kill()
        stop_flag.set()
        monitor_thread.join(0.1)
        print(f"case {num} testing stopped: timeout")
        print()
        print(f"Memory Usage: {memory[0]/1024} KB")
        print("--------------------------------------------------")
        return False
    finally:
        if monitor_thread.is_alive():
            stop_flag.set()
            monitor_thread.join(0.1)
    
    output = result[0].strip()
    error = result[1].strip()
    if error:
        print(error)
    if process.returncode < 0:
        print(output)
        if process.returncode == -11:
            print(f"case {num} testing stopped: segfault")
        else:
            print(f"case {num} testing stopped: terminated by signal {abs(process.returncode)}")
    elif process.returncode != 0:
        print(output)
        print(f"case {num} testing stopped: error code {process.returncode}")

        if lang.count("fsan") > 0:
            print("Summary:", error.split("SUMMARY:")[1].split("\n")[0])
    elif debug:
        print(f"Output for case {num}:\n{output}")
        print(f"Answer:\n{ans.strip()}")
    else:
        print(f"Output for case {num}:\n{output}")
        if output == ans.strip():
            print(f"Correct!")
            success = True
        else:
            print(f"Miss! Expected:\n{ans.strip()}")
    print()        
    print(f"Memory Usage: {memory[0]/1024} KB")
    print("--------------------------------------------------")
    return success

def run_ac(prob_num : int, filename : str, lang : str ,avail : bool) -> bool:
    if (not avail):
        print("Testcase.ac not available for this problem")
        return None
    print("Running testcase.ac ...")
    if lang.count("cpp"):
        lang = "cpp"
    elif lang.count("c"):
        lang = "c"
    elif lang.count("py"):
        lang = "py"
    code = get_code(filename, lang)
    generator, answer = get_testac_id(prob_num)
    if lang.count("c"):
        lang = "cpp"
    url = "https://testcase.ac/api/trpc/runner.stress?batch=1"
    payload = {
        "0": {
            "json": {
                "targetCode": code,
                "problemExternalId": str(prob_num),
                "targetCodeLang": lang,
                "generatorCodeId": generator,
                "correctCodeId": answer,
                "checkerCodeId": None
            },
            "meta": {
                "values": {
                    "checkerCodeId": ["undefined"]
                }
            }
        }
    }
    headers = {'Content-Type': 'application/json', 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    try:
        res = requests.post(url, data=json.dumps(payload), headers=headers)
        result = res.json()[0]
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to testcase.ac: {e}")
        return None
    if result:
        print("\nTestcase.ac Results:")
        # print("Response:", json.dumps(result, indent=4))
        wrong_cases = result["result"]["data"]["json"]["result"]["wrongCases"]
        exec_failed_cases = result["result"]["data"]["json"]["result"]["executionFailedCases"]
        total_cases = int(result["result"]["data"]["json"]["result"]["totalCases"])
        wrong_cases_cnt = int(result["result"]["data"]["json"]["result"]["wrongCasesCount"])
        correct_cases_cnt = total_cases - wrong_cases_cnt
        exec_failed_cnt = int(result["result"]["data"]["json"]["result"]["executionFailedCasesCount"])
        
        if (wrong_cases_cnt == 0 and exec_failed_cnt == 0):
            print(f"Passed {correct_cases_cnt}/{total_cases} testcases")
            print("All testcases passed!")
            return True
        else:
            print(f"Passed {correct_cases_cnt}/{total_cases} testcases")
            print(f"Failed {wrong_cases_cnt} testcases")
            print("Failed testcases:")
            for i, case in enumerate(wrong_cases):
                print(f"Case {i+1}:")
                print(f'Input:\n{case["testcase"]}Output: {case["targetOutput"]}\nExpected: {case["correctOutput"]}')
                print("--------------------------------------------------")
            if exec_failed_cnt > 0:
                print(f"Execution failed {exec_failed_cnt} testcases")
                print("Execution failed testcases:")
                for i, case in enumerate(exec_failed_cases):
                    print(f"Case {i+1}:")
                    print(f'Input:\n{case["testcase"]}')
                    reason = case["reason"]
                    if reason == "RTE":
                        print("Reason: Runtime Error")
                    elif reason == "TLE":
                        print("Reason: Time Limit Exceeded")
                    else:
                        print("Reason: "+ reason)
                    print("--------------------------------------------------")
            return False