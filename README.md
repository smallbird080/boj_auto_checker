# BOJ auto checker

백준 문제의 예제, 반례를 자동으로 테스트합니다.

백준 문제에 제공된 예제와 testcase.ac 채점 결과를 한번에 확인할 수 있도록 제작된 도구입니다.

## Installation

windows에서는 `wsl`을 사용하여 설치하시기 바랍니다.

```bash
cd "your boj source code directory"
git clone https://github.com/smallbird080/boj_auto_checker.git
```

아래와 같은 디렉토리 구조가 되어야 합니다.

```
[BOJ src dir]
├── boj_auto_checker
│   ├── modules
│   │   ├── ...
│   ├── checker.py
│   ├── config.json
│   ├── Makefile
│   └── README.md
├── boj.c
├── boj.cpp
├── boj.py
├── boj.java
└── ...
```

## Usage

```bash
$ python3 boj_auto_checker/checker.py
```

### Commands

```
>> help
Commands:
  !<command>: Run shell command
  help, h: Show this message
  exit, quit, q: Exit the program
  run, r [a,b,t,g]: Run your code
  make, m: Compile the source code
  clean: Remove compiled files
  setl <lang>: Set the main language
  setf <filename>: Set the filename
  info: Display checker information
  prob: Display problem information
  showex, ex, se: Show testcases
```

### Example

실행 시 맨 처음 문제 번호를 입력합니다. (ex. 11657)

```
BOJ Auto Checker
Version 1.1.1

Current filename: boj
Current main language: cpp
Available Languages: 
 c11, c99, cpp, c-fsan, cpp-fsan, java, python

Problem Number: 11657
>> prob
Current Problem Number: 11657
Title: 타임머신
Level: Gold 4
Time Limit: 1.0 sec
Memory Limit: 256 MB
Avg Tries: 3.8227
Success Count: 11704
# Cases: 3
testcase.ac available: True
```

`make` 또는 `m` 명령어를 통해 컴파일을 수행합니다.

```
>> make
g++ -o ../boj ../boj.cpp -O2 -Wall -lm -static -std=gnu++17
```

`run` 또는 `r` 명령어를 통해 실행합니다. 자동으로 수집된 예제를 테스트합니다.

옵션: `a` - 모든 예제 (기본값), `b` - BOJ 제공 예제, `t` - testcase.ac 실행, `g` - 디버깅 모드 (출력 채점 X)

```
>> run
Testing BOJ + testcase.ac

Running case 1...
Output for case 1:
4
3
Correct!

Memory Usage: 8.0 KB
--------------------------------------------------
Running case 2...
Output for case 2:
-1
Correct!

Memory Usage: 8.0 KB
--------------------------------------------------
Running case 3...
Output for case 3:
3
-1
Correct!

Memory Usage: 8.0 KB
--------------------------------------------------
Running testcase.ac ...

Testcase.ac Results:
Passed 100/100 testcases
All testcases passed!
```

실패 예시

```
>> run
Testing BOJ + testcase.ac

Running case 1...
Output for case 1:
5
4
Miss! Expected:
4
3

Memory Usage: 8.0 KB
--------------------------------------------------
Running case 2...
Output for case 2:
-1
Correct!

Memory Usage: 8.0 KB
--------------------------------------------------
Running case 3...
Output for case 3:
4
0
Miss! Expected:
3
-1

Memory Usage: 8.0 KB
--------------------------------------------------

BOJ Results:
Case 1: Fail
Case 2: Pass
Case 3: Fail

Running testcase.ac ...

Testcase.ac Results:
Passed 53/100 testcases
Failed 47 testcases
Failed testcases:
Case 1:
Input:
2 1
2 1 5
Output: 0
Expected: -1
--------------------------------------------------
Case 2:
Input:
2 1
2 1 0
Output: 0
Expected: -1
--------------------------------------------------
Case 3:
Input:
2 1
1 2 4
Output: 5
Expected: 4
--------------------------------------------------
```

fsanitize=address 사용 시

```
>> setl cpp-fsan
>> make
g++ -o ../boj ../boj.cpp -O2 -Wall -lm -std=gnu++17 -fsanitize=address -g

>> r b
Testing BOJ

Running case 1...
=================================================================
==86105==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x603000000058 at pc 0x55e3a81d324e bp 0x7ffffb4b3f40 sp 0x7ffffb4b3f30
WRITE of size 8 at 0x603000000058 thread T0
    #0 0x55e3a81d324d in main ../boj.cpp:31
    #1 0x7f4c0a237d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f4c0a237e3f in __libc_start_main_impl ../csu/libc-start.c:392

<...>

==86105==ABORTING

case 1 testing stopped: error code 1
Summary:  AddressSanitizer: heap-buffer-overflow ../boj.cpp:31 in main

Memory Usage: 8.0 KB
--------------------------------------------------
Running case 2...

<...>

BOJ Results:
Case 1: Fail
Case 2: Fail
Case 3: Fail
```

## Features

기본 언어는 `C++ (gnu++17)`로, 기본 파일명은 `boj`로 설정되어 있습니다. 현재 C/C++, Java, Python을 지원합니다.

등록된 Makefile을 통해 스크립트 내에서 원하는 언어를 컴파일하고 실행할 수 있습니다.

Makefile에 사용된 컴파일 옵션은 [https://help.acmicpc.net/language/info/all](https://help.acmicpc.net/language/info/all) 를 참고하였습니다.

Makefile 수정을 통해 원하는 언어, 컴파일 옵션을 추가할 수 있습니다. (스크립트 내 수정 기능 개발 예정?)

스크립트 내부에서 현재 작성중인 코드의 언어, 파일명을 설정할 수 있습니다. (config.json을 직접 수정할 수도 있습니다.)

`!<command>` 형식을 통해 쉘 명령어를 실행할 수 있습니다.

command history 기능을 지원합니다.

fsanitize=address 옵션을 사용할 수 있습니다. (C/C++). fsan 전체 결과와 함께 summary를 추출하여 보여줍니다.

메모리 사용량은 채점 환경과 다를 수 있습니다. 참고용으로만 사용하기 바랍니다.

## TODO

* [X] 컴파일
* [X] 예제 자동 수집
* [X] 실행
* [X] 결과 확인
* [X] testcase.ac 테스팅 구현
* [X] java, python 구현/시간 보정
* [ ] 언어 추가
* [ ] ...
