import os, subprocess
import json
import requests
from .loader import get_testac_id, get_code

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
    

def run_case(filename : str, num : int, testcase : str, ans : str, time : float, lang : str, debug : bool = False) -> bool:
    print(f"Running case {num}...")
    cmd = [os.path.join(current_dir, f"../../{filename}")]
    if lang.count("py"):
        time = time * 3 + 2
        cmd[0] += ".py"
        cmd = ["python3"] + cmd
    elif lang.count("java"):
        time = time * 2 + 1
        cmd[0] += ".java"
        cmd = ["java"] + cmd
    try:
        result = subprocess.run(
            cmd,
            input=testcase.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=time
        )
    except subprocess.TimeoutExpired:
        print(f"case {num} testing stopped: timeout")
        print()
        return False
    
    output = result.stdout.decode('utf-8').strip()
    error = result.stderr.decode('utf-8').strip()
    if error:
        print(error)
    if result.returncode < 0:
        print(output)
        if result.returncode == -11:
            print(f"case {num} testing stopped: segfault")
        else:
            print(f"case {num} testing stopped: terminated by signal {abs(result.returncode)}")
    elif result.returncode != 0:
        print(output)
        print(f"case {num} testing stopped: error code {result.returncode}")

        if lang.count("fsan") > 0:
            print("Summary:", error.split("SUMMARY:")[1].split("\n")[0])
    elif debug:
        print(f"Output for case {num}:\n{output}")
        print(f"Answer:\n{ans.strip()}")
    else:
        print(f"Output for case {num}:\n{output}")
        if output == ans.strip():
            print(f"Correct!")
            print("--------------------------------------------------")
            return True
        else:
            print(f"Miss! Expected:\n{ans.strip()}")
    print("--------------------------------------------------")
    return False

def run_ac(prob_num : int, filename : str, lang : str ,avail : bool) -> bool:
    if (not avail):
        print("Testcase.ac not available for this problem")
        return None
    print("Running testcase.ac ...")
    if lang.count("c"):
        lang = "cpp"
    elif lang.count("py"):
        lang = "py"
    code = get_code(filename, lang)
    generator, answer = get_testac_id(prob_num)
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
                    print("--------------------------------------------------")
                print(exec_failed_cases)
            return False