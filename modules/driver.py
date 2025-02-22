import os, subprocess

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
    

def run_case(filename : str, num : int, testcase : str, ans : str, time : float, lang : str) -> bool:
    print(f"Running case {num}...")
    try:
        result = subprocess.run(
            [os.path.join(current_dir, f"../../{filename}")],
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

# TODO
def run_ac(avail : bool) -> bool:
    if (not avail):
        print("Testcase.ac not available for this problem")
        return None
    print("Running testcase.ac...")
    print("!! on dev !!")