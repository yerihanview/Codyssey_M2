# 🎯 나만의 퀴즈 게임 — 완결형 매뉴얼 (구조 A · 책임 분리형, macOS)

이 문서 하나만 위에서 아래로 따라 하면 미션이 끝납니다.
구조 A는 클래스가 **3개**입니다: `Quiz`(데이터) · `QuizBank`(보관·저장) · `QuizGame`(진행·화면).
모든 코드는 제가 미리 실행해 정상 동작을 확인했습니다.

---

## 0. 이 매뉴얼 읽는 법

| 기호 | 뜻 |
|---|---|
| 🖥️ | **터미널에 입력**할 명령 |
| 💻 | **코드 파일에 쓸/추가할** 코드 |
| 💡 | **왜 이렇게 하는지** (이해의 핵심) |
| ✅ | 제대로 됐는지 **확인**하는 법 |
| 🔷 | **Git 커밋** |
| 🧠 | **스스로 설명해보기** |

**진행 원칙**
- **한 단계 = 한 커밋.**
- 코드는 `main.py` 하나에 씁니다. `state.json`은 프로그램이 **자동 생성**합니다.
- macOS는 실행 명령이 **`python3`** 입니다.

**최종 파일 구조**
```
my-quiz-game/
├── main.py        ← Quiz, QuizBank, QuizGame
├── state.json     ← 실행 시 자동 생성 (gitignore)
├── .gitignore
├── README.md
└── docs/
    └── screenshots/   ← 실행 화면 캡처 저장
```

**커밋 지도 (총 14개 + 병합 1회)**
```
#1  Chore: 프로젝트 초기 설정
#2  Feat: 메뉴 화면 출력
#3  Feat: 안전한 숫자 입력 처리
#4  Feat: Quiz 클래스 추가
#5  Feat: 기본 퀴즈 5개 추가
#6  Feat: 퀴즈 풀기 기능        ← 브랜치 작업 후 병합
#7  Feat: 퀴즈 추가 기능
#8  Feat: 퀴즈 목록 기능
#9  Feat: 점수 확인 기능
#10 Feat: QuizBank로 보관·저장 책임 분리   ★ 구조 A 핵심
#11 Feat: state.json 저장/불러오기
#12 Feat: 안전 종료 처리
#13 Docs: README 작성
#14 Docs: clone/pull 실습 반영
```

---

# Phase 0 · 준비

## Step 0. Python 3.10+ 설치 & 확인

🖥️ 터미널(`⌘+Space` → `터미널`)에서:
```
python3 --version
```
- `Python 3.10.x` 이상 → 생략
- 아니면 `python.org/downloads`에서 3.10+ 설치 → **새 터미널**에서 재확인

✅ `Python 3.10.x` 이상이 보이면 완료.

---

# Phase 1 · 저장소와 뼈대

## Step 1. GitHub 저장소 만들고 로컬과 연결 → 🔷 #1

**① GitHub에서 빈 저장소 생성**: github.com → **+** → New repository → 이름 `my-quiz-game`, Public, 체크박스 모두 해제 → Create → 주소 복사

**② 로컬 폴더**
🖥️
```
cd ~/Desktop
mkdir my-quiz-game
cd my-quiz-game
```

**③ Git 최초 설정**(처음이면)
🖥️
```
git config --global user.name "본인 이름"
git config --global user.email "본인 GitHub 이메일"
```

**④ `.gitignore`** (VSCode로 폴더 열기: `code .`)
💻 `.gitignore`:
```
__pycache__/
*.pyc
.DS_Store
state.json
```
> 💡 `state.json`은 실행 중 자동 생성되는 데이터라 버전 관리 제외. 덕분에 새로 clone하면 파일이 없어 "파일 없음 → 기본 퀴즈" 경로가 자연히 검증됩니다.

**⑤ `README.md` 뼈대**
💻
```markdown
# 나만의 퀴즈 게임

(작성 예정)
```

**⑥ 첫 커밋 & 푸시**
🖥️
```
git init
git add .
git commit -m "Chore: 프로젝트 초기 설정 (.gitignore, README 뼈대)"
git branch -M main
git remote add origin https://github.com/본인이름/my-quiz-game.git
git push -u origin main
```
> 💡 `init`(저장소 시작) → `add`(장바구니 담기) → `commit`(기록 확정) → `remote add`(GitHub 주소에 origin 별명) → `push`(올리기).

✅ GitHub 새로고침 시 파일이 보이면 성공.

🧠 "add와 commit의 차이는?"

## Step 2. 메뉴 & 입력 처리 → 🔷 #2, #3

### #2 메뉴 출력
💻 `main.py`:
```python
def show_menu():
    print("=" * 40)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def main():
    show_menu()


if __name__ == "__main__":
    main()
```
> 💡 `def`는 함수 정의, `"="*40`은 문자열 40회 반복, `if __name__ == "__main__":`은 "직접 실행 시작 지점".

---
**Lesson __main목적**
 독립적인 프로그램으로도 작동하고, 다른 프로그램의 부품(모듈)으로도 안전하게 재사용될 수 있도록

**Lesson 비유***
실행할 때, 어떻게 오셨어요? 물어보면 
1. 전 메인 자격으로 왔습니다. 
2. 전 import로 호출되어 왔습니다. 
그리고 나서, 아 그러시군요. 1번은 이리로, 2번은 저리로 가세요.

---

✅ `python3 main.py` → 메뉴가 한 번 출력.
🔷 `git add main.py && git commit -m "Feat: 메뉴 화면 출력"`

---
**Lesson 코멘트 컨벤션**
혼자 할 때는 자유지만, 남과 함께할 때는 매너이자 실력이다
 Fix: 버그를 수정했을 때
 Docs: 문서(README 등)만 수정했을 때
 Style: 코드 로직 변경 없이 서식, 세미콜론 누락 등을 수정했을 때
 Refactor: 기능 추가나 버그 수정 없이 코드 구조만 개선했을 때
 Test: 테스트 코드를 추가하거나 수정했을 때

---

### #3 안전한 숫자 입력 + 반복
💻 `show_menu` **위에** 추가:
```python
def ask_int(prompt, low, high):
    """low~high 사이의 정수를 안전하게 입력받는다."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
            continue
        try:
            number = int(raw)
        except ValueError:
            print("⚠️ 숫자를 입력하세요.")
            continue
        if low <= number <= high:
            return number
        print(f"⚠️ {low}~{high} 사이의 숫자를 입력하세요.")
```
💻 `main()`을 교체:
```python
def main():
    while True:
        show_menu()
        choice = ask_int("선택: ", 1, 5)
        if choice == 5:
            print("게임을 종료합니다. 안녕히 가세요!")
            break
        else:
            print(f"[{choice}번 기능은 곧 만듭니다]")
```
> 💡 `while True` 무한 반복, `try/except`로 `int("abc")` 오류 잡기, `continue`(다시 입력) vs `break`(탈출) vs `return`(값 반환+종료). **몇 번 반복할지 모르니 `for`가 아니라 `while`.**

✅ `abc`·빈 엔터·`9` 넣어도 안 죽고 다시 물으면 성공. `5`로 종료.
🔷 `git add main.py && git commit -m "Feat: 안전한 숫자 입력 처리(ask_int)"`

🧠 "continue와 break는 어떻게 다른가?"

---
* 함수 이름이 마음에 안든다. ask_int
- get_choice : 반환값을 명확히 알려준다.
- select_menu : 사용자 경험 중심

* 명명규칙(PEP8: 파이썬 코드 스타일 가이드 )
- snake_case : 함수, 변수
- PascalCase : 클래스
- UPPER_CASE : 상수
- 소문자 : 모듈 및 패키지 

* int(raw) : 숫자 연산을 위해 반드시 정수형으로 변환

* try/except vs. if else
- if/else : 미리 두드려보고 가자. Look Before You Leap
            예상 가능한 비즈니스 로직
            조건에 따라 결과가 달라져야 할 때
- try/except : 일단 지르고 수습하자. Easier to Ask Forgiveness than 
Permission. 파이썬 권장 방식 (가독성:메인 로직과 에러 처리의 명확한 분리)
            내가 통제할 수 없는 외부 상황
            드물게 발생하는 에러
---

# Phase 2 · 데이터 모델

## Step 3. `Quiz` 클래스 → 🔷 #4

💻 `main.py` **맨 위**에 추가:
```python
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question    # 문제
        self.choices = choices      # 선택지 4개 리스트
        self.answer = answer        # 정답 번호 1~4

    def show(self):
        print(self.question)
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")

    def is_correct(self, user_choice):
        return user_choice == self.answer
```
> 💡 클래스 = "관련 데이터(속성)+기능(메서드)"를 묶는 설계도. `__init__`은 생성 시 자동 실행, `self`는 "이 퀴즈 자신". `enumerate(..., start=1)`로 선택지에 번호를 붙임.

✅ 임시 확인(확인 후 삭제): `main()` 호출 전에
```python
q = Quiz("2+2는?", ["3", "4", "5", "6"], 2)
q.show()
print(q.is_correct(2))  # True
```
🔷 `git add main.py && git commit -m "Feat: Quiz 클래스 추가"`

🧠 "self가 없으면 무슨 문제가 생기나?"
- 변수에서 삭제 :
  객체 데이터 사용 불가 > 객체 변수가 아닌 로컬 변수로 인식
- 입력 인자에서 삭제 :
  파이썬은 객체.메서드()를 호출할 때 자동으로 객체 자신을 첫 번째 인자로 입력
  하지만, 받아들일 자리가 없어서 "TypeError" 발생 

---

* 새롭게 정의된 변수 : choice, user_choice
* enumberate : 리스트의 인덱스(i)와 값(choice)을 튜플 형태로 반환
* self를 넣는 이유
- 클래스의 메서드는 메모리 상에 하나만 존재한다. 객체마다 복사하지 않는다.
- 객체는 데이타만 별도로 갖고 있다. 메서드는 모든 객체가 공유한다.
- 클래스의 메서드를 호출할 때에 객체의 정보를 알려줘야 한다. 
- 메서드를 호출하는 시점에 self를 넣지는 않는다.
- 메서드를 실행하는 시점에서는 어떤 객체인지의 정보를 self로 입력받는다.
- Explicit is better than implicit의 철학에 따라 메서드에서 self를 드러냄.

---


## Step 4. 기본 퀴즈 5개 → 🔷 #5

**퀴즈 주제**를 정하세요(예시는 일반 상식 — 원하는 주제로 교체 가능).
💻 `Quiz` 클래스 **바로 아래**:
```python
DEFAULT_QUIZZES = [
    Quiz("태양계에서 가장 큰 행성은?", ["수성", "목성", "화성", "지구"], 2),
    Quiz("대한민국의 수도는?", ["부산", "인천", "서울", "대구"], 3),
    Quiz("물의 화학식은?", ["CO₂", "H₂O", "O₂", "NaCl"], 2),
    Quiz("1년은 몇 개월인가?", ["10개월", "11개월", "12개월", "13개월"], 3),
    Quiz("무지개는 보통 몇 색으로 표현하나?", ["5색", "6색", "7색", "8색"], 3),
]
```
> 💡 `[ ... ]`는 리스트(순서 있는 묶음), 각 `Quiz(...)`는 같은 설계도로 찍은 인스턴스 5개.

✅ 임시: `print(len(DEFAULT_QUIZZES))` → `5`.
🔷 `git add main.py && git commit -m "Feat: 기본 퀴즈 5개 추가"`

---
* List : 여러 개의 데이타를 하나의 묶음으로 관리할 수 있는 자료형
- 대괄호 []를 사용
- 하나의 리스트 내에 서로 다른 유형의 데이타를 담을 수 있다. 
- 크기가 가변적이다.
- 순서가 있다. 
- Indexing: fruits[0], fruits[-]
- Slicing: fruits[0:2]
- 추가 : fruits.append("오렌지")
- 삭제 : fruits.remove("바나나") or del fruits[0]

---

# Phase 3 · 핵심 기능 (브랜치 실습)

> 이 Phase에선 기능을 **함수**로 만듭니다. Phase 4에서 이 함수들을 **QuizBank/QuizGame 두 클래스로 분리**하며 "책임 분리"를 체감합니다.

## Step 5. 퀴즈 풀기 — 🌿 브랜치 작업 → 🔷 #6 + 병합

🖥️ 새 브랜치:
```
git checkout -b feature/play
```
> 💡 `-b`는 "새로 만들며 이동". 이제 여기서 뭘 해도 `main`은 안전.

💻 `show_menu` 아래에 추가:
```python
def play(quizzes):
    if not quizzes:
        print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
        return 0
    print(f"\n📝 퀴즈를 시작합니다! (총 {len(quizzes)}문제)\n")
    score = 0
    for i, quiz in enumerate(quizzes, start=1):
        print("-" * 40)
        print(f"[문제 {i}]")
        quiz.show()
        user_choice = ask_int("정답 입력: ", 1, 4)
        if quiz.is_correct(user_choice):
            print("✅ 정답입니다!")
            score += 1
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
    print("=" * 40)
    print(f"🏆 결과: {len(quizzes)}문제 중 {score}문제 정답!")
    print("=" * 40)
    return score
```
💻 `main()`에서 1번 연결:
```python
def main():
    quizzes = list(DEFAULT_QUIZZES)
    while True:
        show_menu()
        choice = ask_int("선택: ", 1, 5)
        if choice == 1:
            play(quizzes)
        elif choice == 5:
            print("게임을 종료합니다. 안녕히 가세요!")
            break
        else:
            print(f"[{choice}번 기능은 곧 만듭니다]")
```
> 💡 `play(quizzes)`로 목록을 **매개변수**로 넘기고, `return score`로 맞힌 수를 **반환**. `not quizzes`로 빈 목록 처리.

✅ `1` 선택 → 5문제 풀고 결과가 뜨면 성공.
🔷 브랜치에서: `git add main.py && git commit -m "Feat: 퀴즈 풀기 기능"`

🖥️ main으로 병합:
```
git checkout main
git merge feature/play
git push
```
> 💡 `checkout main`(복귀) → `merge feature/play`(합치기). 팀 협업의 기본.

🧠 "브랜치를 나눠 작업하면 뭐가 좋은가?"


---
* git checkout 특정 시점이나 다른 브랜치로 작업 공간을 이동하겠다.
- 의미 : 보관된 많은 코드 중에서, 특정한 버전을 "대여(checkout)"해서 보겠다.
- 다른 브랜치로 이동하기 : git checkout <브랜치명>
- 새로운 브랜치를 만들고, 이동하기 : git checkout -b <새 브랜치명>
- 특정 시점으로 돌아가기 : git checout <커밋_해시_값>
- 요즘은 브랜치 이동은 switch, 특정 시점으로 복구는 restore를 많이 쓴다.
- 안전한 연습장을 만들어서 코드를 수정하고 커밋한다.

* git checkout main + git merge feature/play
- merge : 수정된 부분만 추적해서 합친다. 변경내역(델타)를 기록한다. diff로 비교
- feature/play : 폴더로 같은 유형의 브랜치를 묶는다. (ex, feature, fix)

* git add
- 수정한 파일의 내용을 압축된 이진 파일(Binary Object)로 만든다.
- BLOB (Binary Large OBject)
- 고유 주소를 붙인다. (Hash)
- 데이터 저장 위치 : .git/objects/ 스테이징 영역
- 기록실 : .git/index // index 화일이 있는 가상의 공간 = Staging Area

* git commit
- Staging Area에 모아둔 화일을 영구적인 버전으로 저장
- 파일명단(index)를 바탕으로 디렉토리 지도(Tree)생성 : 폴더 구조 + 파일 상태
- 커밋 객체 생성 : Author, Timestamp, Message, Tree의 고유주소, Parent Pointer 
- 단방향 Linked List

* Working Directory > Staging Area > Local Repository
* 브랜치 옮기기 전에 무조건 해당 브랜치에서 git commit을 해야 한다. 
* 커밋은 현재의 브랜치에 한다.
* A브랜치 이동 > 작업 > 커밋 = 작업 > A브랜치 이동 > 커밋 


* 함수의 순서가 중요하다.
- 스크립트 언어는 앞에서부터 호출한다.
- 내가 호출하는 함수가 먼저 정의되어야 한다.
- if __name__ == "__main__": 가 파일 맨 마지막에 위치하는 이유이다.

* enumerate : 번호 붙여주는 기계, start = 1 // 1번부터 시작해. ++도 할께.
* for문은 리스트에서 알맹이만 하나씩 꺼내는 방식 (숫자를 세지 않는다.)

* quizzes = list(DEFAULT_QUIZZES)
- 이미 DEFAULT_QUIZZES는 리스트이다.
- 원본 데이타 보호를 위해 복사본을 만들어서 사용한다.

* ask_int : 메뉴 번호 선택, 퀴즈 정답 선택 두가지 용도로 사용한다.
---

## Step 6. 퀴즈 추가 → 🔷 #7
💻 `play` 아래:
```python
def add_quiz(quizzes):
    print("\n📌 새로운 퀴즈를 추가합니다.")
    question = input("문제를 입력하세요: ").strip()
    if question == "":
        print("⚠️ 문제가 비어 있어 취소합니다.")
        return
    choices = []
    for i in range(1, 5):
        choice = input(f"선택지 {i}: ").strip()
        if choice == "":
            print("⚠️ 선택지가 비어 있어 취소합니다.")
            return
        choices.append(choice)
    answer = ask_int("정답 번호 (1-4): ", 1, 4)
    quizzes.append(Quiz(question, choices, answer))
    print("✅ 퀴즈가 추가되었습니다!")
```
💻 `main()` 분기에 추가: `elif choice == 2: add_quiz(quizzes)`
> 💡 `range(1,5)`는 1~4(4 포함, 5 제외). 리스트는 수정 가능(mutable)이라 함수 안 `append`가 바깥에도 반영.

✅ `2`로 추가 → `1`(풀기)에서 방금 문제가 나오면 성공.
🔷 `git add main.py && git commit -m "Feat: 퀴즈 추가 기능"`

---
* range(1,5) : 1에서 4까지만, end-start하면 쉽게 계산 (5-1=4번 반복)
* choices = []은 for문 밖에서 미리 선언해야 한다.
---

## Step 7. 퀴즈 목록 → 🔷 #8
💻 `add_quiz` 아래:
```python
def list_quizzes(quizzes):
    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return
    print(f"\n📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print("-" * 40)
    for i, quiz in enumerate(quizzes, start=1):
        print(f"[{i}] {quiz.question}")
    print("-" * 40)
```
💻 `main()`: `elif choice == 3: list_quizzes(quizzes)`
🔷 `git add main.py && git commit -m "Feat: 퀴즈 목록 기능"`

## Step 8. 점수 확인 → 🔷 #9
💻 `list_quizzes` 아래:
```python
def show_score(best_score, has_played):
    if not has_played:
        print("아직 퀴즈를 풀지 않았습니다.")
        return
    print(f"\n🏆 최고 점수: {best_score}문제 정답")
```
💻 `main()`을 교체(점수 상태 추적):
```python
def main():
    quizzes = list(DEFAULT_QUIZZES)
    best_score = 0
    has_played = False
    while True:
        show_menu()
        choice = ask_int("선택: ", 1, 5)
        if choice == 1:
            score = play(quizzes)
            has_played = True
            if score > best_score:
                best_score = score
                print("🎉 새로운 최고 점수입니다!")
        elif choice == 2:
            add_quiz(quizzes)
        elif choice == 3:
            list_quizzes(quizzes)
        elif choice == 4:
            show_score(best_score, has_played)
        elif choice == 5:
            print("게임을 종료합니다. 안녕히 가세요!")
            break
```
> 💡 `play`가 돌려준 `score`로 `best_score`를 갱신. `has_played`는 참/거짓(`bool`) 스위치.

✅ 풀고 `4` → 최고점수 표시. 안 풀고 `4` → "아직 안 풀었다".
🔷 `git add main.py && git commit -m "Feat: 점수 확인 기능"`

🧠 지금 `main()`이 `quizzes`, `best_score`, `has_played` 세 상태를 들고 모든 함수에 넘겨주죠? **이걸 두 클래스로 나눠 정리합니다.**

> 🔎 **여기까지 `main.py` 순서**: `class Quiz` → `DEFAULT_QUIZZES` → `ask_int` → `show_menu` → `play` → `add_quiz` → `list_quizzes` → `show_score` → `main` → `if __name__...`

--- 2026.08.03 13:49

---

* 나 돌아갈래
- git log -oneline : 돌아가고 싶은 과거 커밋의 앞자리 7글자 주소 찾기
- git checkout a1b2c3d. /최신 버전 git switch --detach <커밋해시>
- git reset --hard <돌아갈_과거_커밋해시>

---

# Phase 4 · 책임 분리와 영속성

## Step 9. `QuizBank` + `QuizGame`로 분리 → 🔷 #10 ★

> 💡 **왜 두 클래스인가?** 지금 `main()`이 데이터(`quizzes`, `best_score`)를 들고 모든 함수에 넘깁니다. 이걸 **역할별로 두 클래스에** 나눕니다.
> - **`QuizBank`**: 퀴즈 목록·최고점수를 **보관**하고 다루는 곳 (데이터 담당)
> - **`QuizGame`**: 메뉴·풀기·화면을 **진행**하는 곳 (진행 담당). 데이터가 필요하면 `self.bank`에 시킴

💻 `show_menu` / `play` / `add_quiz` / `list_quizzes` / `show_score` / `main` **함수 6개를 통째로 지우고**, 그 자리에 아래 **두 클래스**를 넣습니다. (`class Quiz`, `DEFAULT_QUIZZES`, `ask_int`는 그대로 둡니다.)

```python
class QuizBank:
    """퀴즈 보관 + 최고점수 (데이터 담당). 저장 기능은 Step 10에서 추가."""

    def __init__(self):
        self.quizzes = list(DEFAULT_QUIZZES)
        self.best_score = 0

    def is_empty(self):
        return len(self.quizzes) == 0

    def add(self, quiz):
        self.quizzes.append(quiz)

    def update_best_score(self, score):
        """더 높으면 갱신하고 True, 아니면 False."""
        if score > self.best_score:
            self.best_score = score
            return True
        return False


class QuizGame:
    """메뉴·풀기·점수 진행 + 화면 (진행 담당)."""

    def __init__(self):
        self.bank = QuizBank()
        self.has_played = False

    def show_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def play(self):
        if self.bank.is_empty():
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return
        quizzes = self.bank.quizzes
        print(f"\n📝 퀴즈를 시작합니다! (총 {len(quizzes)}문제)\n")
        score = 0
        for i, quiz in enumerate(quizzes, start=1):
            print("-" * 40)
            print(f"[문제 {i}]")
            quiz.show()
            user_choice = ask_int("정답 입력: ", 1, 4)
            if quiz.is_correct(user_choice):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
        print("=" * 40)
        print(f"🏆 결과: {len(quizzes)}문제 중 {score}문제 정답!")
        self.has_played = True
        if self.bank.update_best_score(score):
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = input("문제를 입력하세요: ").strip()
        if question == "":
            print("⚠️ 문제가 비어 있어 취소합니다.")
            return
        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ").strip()
            if choice == "":
                print("⚠️ 선택지가 비어 있어 취소합니다.")
                return
            choices.append(choice)
        answer = ask_int("정답 번호 (1-4): ", 1, 4)
        self.bank.add(Quiz(question, choices, answer))
        print("✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        if self.bank.is_empty():
            print("등록된 퀴즈가 없습니다.")
            return
        quizzes = self.bank.quizzes
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)")
        print("-" * 40)
        for i, quiz in enumerate(quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)

    def show_score(self):
        if not self.has_played:
            print("아직 퀴즈를 풀지 않았습니다.")
            return
        print(f"\n🏆 최고 점수: {self.bank.best_score}문제 정답")

    def run(self):
        while True:
            self.show_menu()
            choice = ask_int("선택: ", 1, 5)
            if choice == 1:
                self.play()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                print("게임을 종료합니다. 안녕히 가세요!")
                break
```
💻 파일 **맨 아래** 교체:
```python
if __name__ == "__main__":
    QuizGame().run()
```
> 💡 달라진 점: 함수들의 `quizzes` 매개변수가 사라지고, 데이터는 **`self.bank`**가 들고 있습니다. 최고점수 갱신은 `self.bank.update_best_score(score)` **한 줄** — 비교 로직이 QuizBank 안으로 숨었습니다(캡슐화). `QuizGame`은 "데이터 세부는 모르고 은행에 시키기만" 합니다.

✅ 실행 → **이전과 동작 동일**, 구조만 또렷해지면 성공.
🔷 `git add main.py && git commit -m "Feat: QuizBank로 보관·저장 책임 분리"`

🧠 "QuizBank와 QuizGame은 각각 뭘 책임지나?"

--- 2026.08.03 14:05 : git push 완료

## Step 10. `state.json` 저장/불러오기 (QuizBank에) → 🔷 #11

**① `Quiz`에 변환 메서드** (객체 ↔ 딕셔너리)
💻 `Quiz` 안 `is_correct` 아래:
```python
    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"])
```

---
* to_dict : Quiz 객체를 Dictionary (Key-Value Pair) 데이터로 변환
- Dictionary 변환은 Serialization의 첫 단계
- Serialization : 메모리속에 있는 복잡한 입체 구조의 데이타를 네트워크에 보낼 수 있는 형태(0, 1의 반복)로 바꾸는 행위

* from_dict : Dictionary (Key-Value Pair) 데이터를 Quiz객체로 변환

* @classmethod
- 객체없이 클래스 이름을 직접 호출할 수 있다는 표시
- Decorator는 함수의 일반적인 성격을 바꿔주는 장치
- Quiz.from_dict(data) : 객체 대신 클래스 이름 사용

* cls
- 클래스 자신을 가리키는 첫번째 인자. self와 동일한 역할'인잇

---


**② 파일 맨 위에 import + 상수**
💻 `main.py` 첫 줄:
```python
import json
import os

STATE_FILE = "state.json"
```

---

* import 필요한 도구 불러오기
- json : 직렬화 수행 도구
- os : 찾고 있는 파일이 실제로 존재하는가?를 확인할 때
* STATE_FILE : 상수 선언

---

**③ `QuizBank`에 load/save 추가하고 `__init__` 수정**
💻 `QuizBank.__init__`을 교체:
```python
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.load()
```
💻 `__init__` 아래에 추가:
```python
    def load(self):
        if not os.path.exists(STATE_FILE):
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = 0
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            return
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(d) for d in data["quizzes"]]
            self.best_score = data["best_score"]
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score})")
        except (json.JSONDecodeError, KeyError, OSError):
            print("⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = 0

    def save(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            print("⚠️ 저장 중 오류가 발생했습니다.")
```
---

* with open(...) as f : 화일을 열고, 작업 끝나면 안전하게 닫는다.
- 파일을 열고, 안 닫으면 메모리 누수가 발생하는 문제 원천 차단
- with : ~한 상태에서. 이 블록 안에서는 이 상태가 유지된다.
- 멀티쓰레드에서 데이타 충돌을 막는 역할도 한다. file에 대한 lock을 건다.

* List Comprehension
- [Quiz.from_dict(d) for d in data["quizzes"]] 
   ----------------  ------------------------
          결과물               for 루프 
- 리스트에서 퀴즈 하나씩 뽑아서 Quiz 객체를 만든다.
- "파일에서 읽어온 퀴즈 딕셔너리 데이터 리스트에서 딕셔너리 하나(d)를 쏙 꺼내와서,"
- "딕셔너리(d)를 Quiz 객체로 만든 뒤, 최종 리스트에 채워 넣어라!"
* except : 3가지 유형의 에러에 대해서 동일하게 처리해라.

---

**④ 데이터가 바뀔 때 저장** — `add`와 `update_best_score`가 저장하도록 교체:
💻
```python
    def add(self, quiz):
        self.quizzes.append(quiz)
        self.save()

    def update_best_score(self, score):
        if score > self.best_score:
            self.best_score = score
            self.save()
            return True
        return False
```
> 💡 **파일 담당을 QuizBank 하나로 못 박은 이유**: 파일을 여러 클래스가 각자 건드리면 충돌·꼬임이 나기 쉽습니다. **저장 지점을 한 곳(QuizBank)으로** 두면 안전하고, 나중에 저장 방식을 바꿔도 여기만 고치면 됩니다.
> - `with open(..., encoding="utf-8")` + `ensure_ascii=False` → 한글 안 깨짐
> - `except (JSONDecodeError, KeyError, OSError)` → 깨진 파일/이상한 형식/읽기 실패에도 복구

✅ 퀴즈 추가·종료 → **다시 실행** → "불러왔습니다 (퀴즈 6개…)" + 추가한 퀴즈 유지 + 폴더에 `state.json` 생성.
🔷 `git add main.py && git commit -m "Feat: state.json 저장/불러오기"`

🧠 "파일을 QuizBank 하나만 만지게 한 이유는?"

--- 2026.08.05 19:02

## Step 11. 안전 종료 → 🔷 #12
💻 `QuizGame.run`을 교체:
```python
    def run(self):
        try:
            while True:
                self.show_menu()
                choice = ask_int("선택: ", 1, 5)
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    print("게임을 종료합니다. 안녕히 가세요!")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n프로그램을 안전하게 종료합니다.")
        finally:
            self.bank.save()
```
> 💡 `Ctrl+C`(KeyboardInterrupt)·입력 끊김(EOFError)을 잡아 안내 후 종료. `finally`는 무조건 실행되므로 여기서 마지막 저장 → 데이터 손실 방지.

✅ 실행 중 `Ctrl+C` → 빨간 오류 대신 "안전하게 종료합니다".
🔷 `git add main.py && git commit -m "Feat: 안전 종료 처리(Ctrl+C/EOF)"`

> 🎉 **프로그램 완성.** `main.py` 최종 순서: `import` → `STATE_FILE` → `class Quiz` → `DEFAULT_QUIZZES` → `ask_int` → `class QuizBank` → `class QuizGame` → `if __name__ == "__main__": QuizGame().run()`

---

# Phase 5 · 문서화와 Git 마무리

## Step 12. README.md 작성 → 🔷 #13 + 최종 push

💻 `README.md`:
```markdown
# 🎯 나만의 퀴즈 게임

## 프로젝트 개요
터미널에서 동작하는 콘솔 퀴즈 게임. 퀴즈를 풀고 추가하고 목록·최고점수를 확인하며,
데이터는 파일에 저장되어 재실행해도 유지됩니다.

## 퀴즈 주제와 선정 이유
- 주제: (예: 일반 상식 / 영화 …)
- 선정 이유: (한두 문장)

## 실행 방법
​```
python3 main.py
​```
(Python 3.10 이상)

## 기능 목록
- 퀴즈 풀기 / 추가 / 목록 / 점수 확인
- 잘못된 입력·빈 입력·Ctrl+C 안전 처리

## 파일 구조
​```
my-quiz-game/
├── main.py       # Quiz, QuizBank, QuizGame
├── state.json    # 자동 생성 데이터
├── .gitignore
├── README.md
└── docs/screenshots/
​```

## 데이터 파일 설명 (state.json)
- 위치: 프로젝트 루트 / 역할: 퀴즈·최고점수를 UTF-8 JSON으로 저장·불러오기
- 없을 때: 기본 퀴즈로 시작, 종료 시 생성 / 손상 시: 안내 후 기본 복구
- 스키마:
​```json
{ "quizzes": [ { "question": "문제", "choices": ["1","2","3","4"], "answer": 2 } ], "best_score": 3 }
​```

## 실행 화면
![메뉴](docs/screenshots/menu.png)
![풀기](docs/screenshots/play.png)
![추가](docs/screenshots/add_quiz.png)
![점수](docs/screenshots/score.png)
```
> 💡 마지막 **실행 화면** 섹션과 `docs/screenshots/` 경로는 미션 제출 요건입니다. 이미지는 Step 14에서 캡처해 넣습니다.

🔷 `git add README.md && git commit -m "Docs: README 작성" && git push`

## Step 13. clone / pull 실습 → 🔷 #14
🖥️ ① 다른 폴더에 복제:
```
cd ~/Desktop
git clone https://github.com/본인이름/my-quiz-game.git quiz-clone
cd quiz-clone
```
💻 복제본 `README.md` 맨 아래 한 줄 추가 (예: `# clone/pull 실습 완료`)
🖥️ ② 복제본에서:
```
git add README.md
git commit -m "Docs: clone/pull 실습 반영"
git push
```
🖥️ ③ 원래 폴더에서 당겨오기:
```
cd ~/Desktop/my-quiz-game
git pull
```
✅ 원래 폴더 README에 추가한 줄이 보이면 clone·pull 성공.
> 💡 `clone`=원격 통째 복제, `pull`=원격 변경을 로컬로 당김.

🧠 "clone과 pull은 각각 언제 쓰나?"

## Step 14. 제출물 정리
🖥️ 스크린샷은 `docs/screenshots/`에 `menu.png`·`play.png`·`add_quiz.png`·`score.png`로 저장.
🖥️ 커밋 그래프:
```
git log --oneline --graph --all
```
**제출 체크리스트**
- [ ] 저장소 URL
- [ ] 환경 스크린샷 (VSCode, `python3 --version`, `git config`)
- [ ] 실행 스크린샷 4장 (메뉴/풀기/추가/점수)
- [ ] `git log --oneline --graph` 스크린샷

**최종 요건 점검**: 클래스 3개 ✅ / state.json UTF-8·복구 ✅ / 주제 5개+ ✅ / 커밋 14개+ ✅ / 브랜치·병합 ✅ / clone·pull ✅ / Git 7종 ✅ / README 6항목+스크린샷 ✅

---

# Phase 6 · 보너스 (선택)
각각 **새 브랜치**에서 → 병합.
- **랜덤 출제**: `QuizGame.play`에서 `import random` 후 목록 복사본을 `random.shuffle`
- **문제 수 선택**: `play` 진입 시 `ask_int`로 개수 입력
- **힌트**: `Quiz`에 `hint` 속성 추가, 점수 차감
- **퀴즈 삭제**: **QuizBank**에 `delete(index)` 추가 → `pop` 후 `save`
- **점수 히스토리**: **QuizBank**가 저장하는 데이터에 `history` 배열 추가
> 구조 A에서는 데이터 관련은 **QuizBank**, 진행/화면 관련은 **QuizGame**에 추가하면 자리가 명확합니다.

---

# 부록 A. Git 치트시트

| 명령 | 하는 일 |
|---|---|
| `git init` | 폴더를 저장소로 |
| `git add .` | 변경 스테이징 |
| `git commit -m "..."` | 기록 확정 |
| `git push` / `git pull` | 올리기 / 당기기 |
| `git checkout -b 이름` / `git checkout main` | 브랜치 생성·이동 / main 이동 |
| `git merge 브랜치` | 병합 |
| `git clone 주소` | 복제 |
| `git status` | 현재 변경 확인 (수시로) |
| `git log --oneline --graph --all` | 이력 그래프 |

커밋 관례: `Feat:` `Fix:` `Docs:` `Refactor:` `Chore:`

# 부록 B. 자주 나는 오류

| 증상 | 해결 |
|---|---|
| `python: command not found` | macOS는 `python3` |
| `IndentationError` | 들여쓰기 공백 4칸 통일 (탭/공백 혼용 금지) |
| 한글이 `\uc218…`로 저장 | `json.dump(..., ensure_ascii=False)` |
| `AttributeError: 'QuizGame' has no attribute 'quizzes'` | 구조 A에선 `self.bank.quizzes`로 접근 (데이터는 은행에) |
| push했는데 안 보임 | `git status`로 커밋 확인 후 `git push` |

막히면 **단계 번호 + 화면(또는 오류 메시지)**를 저에게 주세요.
