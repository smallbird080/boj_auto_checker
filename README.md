# BOJ auto checker

백준 문제의 예제, 반례를 자동으로 테스트합니다.

## Installation

windows에서는 `wsl`을 사용하여 설치하시기 바랍니다.

```bash
cd "<your boj source code directory>"
git clone https://github.com/smallbird080/boj_auto_checker.git
```

아래와 같은 디렉토리 구조가 되어야 합니다.

```
<BOJ src dir>
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

```
>> help
Commands:
  !<command>: Run shell command
  help, h: Show this message
  exit, quit, q: Exit the program
  run, r [a,b,t]: Run the program
  make, m: Compile the source code
  setl <lang>: Set the main language
  setf <filename>: Set the filename
  info: Display information
```

```
>> info
BOJ Auto Checker
Version 1.0

Current filename: boj
Current main language: cpp
Available Languages: 
 c11, c99, cpp, c-fsan, cpp-fsan, java, python

>> make
g++ -o ../boj ../boj.cpp -O2 -Wall -lm -static -std=gnu++17
```

## Features

기본 언어는 `C++ (gnu++17)`로, 기본 파일명은 `boj`로 설정되어 있습니다. 현재 C/C++, Java, Python을 지원합니다.

등록된 Makefile을 통해 스크립트 내에서 원하는 언어를 컴파일하고 실행할 수 있습니다.

Makefile에 사용된 컴파일 옵션은 [https://help.acmicpc.net/language/info/all](https://help.acmicpc.net/language/info/all) 를 참고하였습니다.

Makefile 수정을 통해 원하는 언어, 컴파일 옵션을 추가할 수 있습니다. (스크립트 내 수정 기능 개발 예정?)

스크립트 내부에서 현재 작성중인 코드의 언어, 파일명을 설정할 수 있습니다. (config.json을 직접 수정할 수도 있습니다.)

`!<command>` 형식을 통해 쉘 명령어를 실행할 수 있습니다.

command history 기능을 지원합니다.

## TODO

* [X] 컴파일
* [ ] 예제 자동 수집
* [ ] 실행
* [ ] 결과 확인
* [ ] 언어 추가
* [ ] ...
