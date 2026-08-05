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