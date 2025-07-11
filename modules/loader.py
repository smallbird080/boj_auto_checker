import os
import requests
from bs4 import BeautifulSoup as bs

current_dir = os.path.dirname(os.path.abspath(__file__))

levels = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby"]
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

class Problem:
    def __init__(self, prob_num, title, time_limit : float, mem_limit : str, level : int, avg_tries : float, success_cnt : int, cases: int, testcases : list[str], answers : list[str]):
        self.prob_num = prob_num
        self.title = title
        self.time_limit = time_limit
        self.mem_limit = mem_limit
        self.level = level
        self.avg_tries = avg_tries
        self.success_cnt = success_cnt
        self.cases = cases
        self.testcases = testcases
        self.answers = answers
        
        url = "https://testcase.ac/api/extension/problems"
        res = requests.get(url).json()
        availables = list(map(int, res["existProblemIds"]))
        self.ac = prob_num in availables

def get_available_langs() -> list:
    result = []
    with open(os.path.join(current_dir, "../Makefile"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.endswith(":\n") and line != "clean:\n":
                result.append(line.split(":")[0])
    return result

def get_problem(prob_num: int) -> Problem:
    solvedac = f"https://solved.ac/api/v3/problem/show?problemId={prob_num}"
    res = requests.get(solvedac).json()
    title = res["titles"][0]["title"]
    lev = res["level"]
    if lev == 0:
        level = "Unrated"
    else:
        tier = (lev - 1) // 5
        subtier = 5 - (lev - 1) % 5
        level = levels[tier] + " " + str(subtier)
    avg_tries = res["averageTries"]
    success_cnt = res["acceptedUserCount"]

    url = f"https://www.acmicpc.net/problem/{prob_num}"
    session = requests.Session()
    response = session.get(url, headers=headers)
    session.close()
    soup = bs(response.text, 'html.parser')
    try: 
        time_limit = float(soup.select_one("#problem-info > tbody > tr > td:nth-child(1)").text.split()[0])
        mem_limit = soup.select_one("#problem-info > tbody > tr > td:nth-child(2)").text
        sample_inputs = soup.select('[id^="sample-input-"]')
        sample_input_texts = [element.text.replace("\r","") for element in sample_inputs]
        sample_outputs = soup.select('[id^="sample-output-"]')
        sample_output_texts = [element.text.replace("\r","") for element in sample_outputs]
        return Problem(
            prob_num,
            title,
            time_limit,
            mem_limit,
            level,
            avg_tries,
            success_cnt,
            len(sample_input_texts),
            sample_input_texts,
            sample_output_texts
        )
    except:
        print("Failed to fetch acmicpc.net")
        print("try again later")
        return None

def get_code(filename : str, lang : str) -> str:
    if lang.count("cpp"):
        lang = "cpp"
    elif lang.count("c"):
        lang = "c"
    elif lang.count("py"):
        lang = "py"
    with open(os.path.join(current_dir, f"../../{filename}.{lang}"), 'r') as f:
        code = f.read()
    return code

def get_testac_id(prob_num: int) -> tuple[int,int]:
    url = "https://testcase.ac/problems/"+str(prob_num)
    res = requests.get(url, headers=headers)

    import re

    generator_match = re.search(r'generatorCodes.*?id.*?(\d+)', res.text)
    if generator_match:
        generator = int(generator_match.group(1))
    else:
        print("Failed to find generator ID")
        return None, None
    
    answer_match = re.search(r'correctCodes.*?id.*?(\d+)', res.text)
    if answer_match:
        answer = int(answer_match.group(1))
    else:
        print("Failed to find answer ID")
        return None, None
    
    return generator, answer