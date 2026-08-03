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

DEFAULT_QUIZZES = [
    Quiz("태양계에서 가장 큰 행성은?", ["수성", "목성", "화성", "지구"], 2),
    Quiz("대한민국의 수도는?", ["부산", "인천", "서울", "대구"], 3),
    Quiz("물의 화학식은?", ["CO₂", "H₂O", "O₂", "NaCl"], 2),
    Quiz("1년은 몇 개월인가?", ["10개월", "11개월", "12개월", "13개월"], 3),
    Quiz("무지개는 보통 몇 색으로 표현하나?", ["5색", "6색", "7색", "8색"], 3),
]

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

if __name__ == "__main__":
    main()

    